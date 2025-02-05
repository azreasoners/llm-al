import openai
from keys import API_KEY,ORG_KEY
import pickle
import os
import argparse
from argparse import RawTextHelpFormatter
import numpy as np
from utils_cplus2asp import run_cplus2asp, process_errors, clean_signature, clean_query
from prompts import knowledge_gen, sign_gen, rule_gen, feedback_qsat, sq, sq_feedback
from utils import read_env2, write_intermediate3, save_cache, process_hint, LLM, create_output_directory, satisfiability_check, get_feedback, get_feedback2, get_feedback_main


openai.api_key= API_KEY
openai.organization = ORG_KEY


parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument('--o', type=str, help='the output file name')
parser.add_argument("--model", type=str, help = '{o1-preview, gpt-4o, o3-mini}', default = 'o1-preview')
parser.add_argument("--task", type=str, help = 'Problem to run.', required=True)
parser.add_argument("--max_updates", type=str, help = 'Maximum number of steps for LLM revision.', default = 8)
parser.add_argument("--concurrency", action="store_true", help="Cplus2ASP will run with concurrent actions allowed.")
args = parser.parse_args()


args.main_query_max_step = 130
args.maxAdditive = 6 # queries can take a long time if the maxAdditive is larger than needed
args.concurrency = False

if not args.o:
    args.o= args.task

model = args.model
max_updates = args.max_updates

if f'prompt_cache_{model}.pickle' in os.listdir():
    with open(f'prompt_cache_{model}.pickle', 'rb') as handle:
        prompt_cache = pickle.load(handle)
else:
    prompt_cache = dict()



inputs_path, output_path, input_prompts_path = create_output_directory(model, args)

paths = [inputs_path, input_prompts_path, output_path]

if __name__ == '__main__':
    
    problem_logs, total_usage = [], []
    
    for prob_name in range(1):
        

        print('Running...')
    
        # read environment
        prob_desc, hint, query = read_env2(args.task, with_query= True)
        
        input_string = ('\n'+'-'*70+'\n\n\n\n').join([prob_desc, hint, query])

        hint = process_hint(hint)
        
        write_intermediate3(inputs_path, prob_desc, 'Problem Description', 0, -1)
        write_intermediate3(inputs_path, hint, 'Signature Description', 0, -1)
        write_intermediate3(inputs_path, query, 'Query', 0, -1)
        
        
        # Signature Generation
        sign_gen_prompt = sign_gen.replace('<DOMAIN>',prob_desc).replace('<HINT>',hint)
        outputs, prompt_cache, total_usage = LLM(prompt = sign_gen_prompt, step = 'signature generation', model = model, update_idx = 0, prompt_cache = prompt_cache, total_usage = total_usage, paths= paths)
        domain, actions_constants = outputs
        
        # Knowledge Generation
        knowledge_gen_prompt = knowledge_gen.replace('<PROBLEM DESCRIPTION>',prob_desc).replace('<DOMAIN>',domain).replace('<HINT>',hint).replace('<ACTIONS AND CONSTANTS>',actions_constants)
        outputs, prompt_cache, total_usage = LLM(prompt = knowledge_gen_prompt, step = 'knowledge generation', model = model, update_idx = 0, prompt_cache = prompt_cache, total_usage = total_usage, paths= paths)
        knowledge = outputs[0]


        # Rule and Query Generation
        rule_gen_prompt = rule_gen.replace('<PROBLEM DESCRIPTION>', prob_desc).replace('<HINT>',hint).replace('<DOMAIN>',domain).replace('<CONSTRAINTS>',knowledge).replace('<KEPT KNOWLEDGE>','').replace('<KEPT RULES>','').replace('<ACTIONS AND CONSTANTS>',actions_constants).replace('<QUERY>',query)
        outputs, prompt_cache, total_usage = LLM(prompt = rule_gen_prompt, step = 'rule and query generation', model = model, update_idx = 0, prompt_cache = prompt_cache, total_usage = total_usage, paths= paths)
        bc_constraints, query_bc = outputs
        
        
        update_idx=0
        
        domain = clean_signature(domain)
        prog_wo_query = domain.replace('BC+ Signature:','') + '\n\n' + bc_constraints
        
        
        write_intermediate3(output_path, prog_wo_query + '\n\n' + query_bc, 'Initial BC+ Program', 0, 4 + update_idx)
        main_query = clean_query(query_bc)
        
        # Satisfiability Check
        passed = False
        while not passed and update_idx<max_updates:
            #breakpoint()
            sat_output, passed, errs, sample_queries_list_qsat, feedbacks_qsat, prog_num = satisfiability_check(prog_wo_query, args)
            
            if not passed:
                if sat_output == 'False': #unsatisfiable
                    pass
                else: # syntax error
                    err_to_use, errs_dict, err_first, all_undeclared = process_errors(errs)
                
                cplus2asp_feedback_all = ''.join([sample_query + '\n\nCplus2ASP Output:\n\n' + feedback + '\n\n' for sample_query, feedback in zip(sample_queries_list_qsat, feedbacks_qsat)])
                write_intermediate3(output_path, cplus2asp_feedback_all, 'Satisfiability Check Feedback', 0, 5 + update_idx, 1)
                sample_query_feedback_prompt = feedback_qsat.replace('<PROBLEM DESCRIPTION>', prob_desc).replace('<BC+ PROGRAM>',prog_wo_query).replace('<CONSTRAINTS>',bc_constraints).replace('<FEEDBACK>',cplus2asp_feedback_all).replace('<BC QUERY>',query_bc).replace('<QUERY>',query)
                
                # LLM revision
                outputs, update_idx, prompt_cache, total_usage = LLM(prompt = sample_query_feedback_prompt, step = 'satisfiability check', update_idx = update_idx, model = model, prompt_cache = prompt_cache, total_usage = total_usage, paths = paths)
                prog_wo_query, query_bc = outputs
                
                main_query = query_bc
        
        
        if update_idx >= max_updates:
            break
        
        # Sample Query Generation
        sample_query_prompt = sq.replace('<DOMAIN>',domain).replace('<PROBLEM DESCRIPTION>', prob_desc).replace('<QUERY>',query).replace('<CONSTRAINTS>',bc_constraints).replace('<RULES TO REVISE>', '').replace('<REVISED RULES GENERATED>', '').replace('<ACTIONS AND CONSTANTS>',actions_constants).replace('<BC QUERY>',main_query)
        outputs, update_idx, prompt_cache, total_usage = LLM(prompt = sample_query_prompt, step = 'sample query generation', model = model, update_idx = update_idx, prompt_cache = prompt_cache, total_usage = total_usage, paths=paths)
        sample_queries_list = outputs[0]
        
        
        # Run BC+ Reasoner on sample queries to get feedback
        feedbacks = []
        
        for sample_query in sample_queries_list:
            # run sample query and get feedback
            feedback, extra_details, maxAdditive_line = get_feedback(sample_query, prog_wo_query, args)
            feedbacks.append(feedback + extra_details)
        
        # Run BC+ Reasoner on main query to get feedback
        main_query_feedback, prog_num = get_feedback_main(prog_wo_query, main_query, maxAdditive_line, update_idx, args)
        
        cplus2asp_feedback_all = ''.join([sample_query + '\n\nCplus2ASP Output:\n\n' + feedback + '\n\n' for sample_query, feedback in zip(sample_queries_list, feedbacks)])
        write_intermediate3(output_path, cplus2asp_feedback_all + '\n\n' + main_query_feedback, 'Sample Queries Cplus2ASP Feedback', 0, 6 + update_idx, 1)
        
        
        old_prog_wo_query = ''
        while update_idx < max_updates:
            
            # give feedback to LLM
            sample_query_feedback_prompt = sq_feedback.replace('<PROBLEM DESCRIPTION>', prob_desc).replace('<BC+ PROGRAM>',prog_wo_query).replace('<QUERY>',query).replace('<CONSTRAINTS>',bc_constraints).replace('<FEEDBACK>',cplus2asp_feedback_all).replace('<BC QUERY>',main_query).replace('<FEEDBACK MAIN QUERY>', main_query_feedback)
            outputs, segments_changed, update_idx, prompt_cache, total_usage = LLM(prompt = sample_query_feedback_prompt, step = 'sample and main query feedback', update_idx = update_idx, model = model, prompt_cache = prompt_cache, total_usage = total_usage, paths = paths)
            prog_wo_query, main_query, sample_queries, sample_queries_list = outputs
            
            if prog_wo_query == old_prog_wo_query:
                segments_changed[0]=0
            old_prog_wo_query = prog_wo_query

            
            if any(segments_changed):
                program_changed = True
            else:
                program_changed = False
                break
            
            # Run query to check satisfiability and possibly use feedback            
            sat_output, passed, errs, sample_queries_list_qsat, feedbacks_qsat, prog_num = satisfiability_check(prog_wo_query, args)

            if passed:
                use_sat_feedback = False
            else:
                use_sat_feedback = True

            feedbacks = []
            for sample_query in sample_queries_list:
                feedback, extra_details, maxAdditive_line = get_feedback2(sample_query, prog_wo_query, args)
                feedbacks.append(feedback)
            if use_sat_feedback:
                feedbacks_to_use = feedbacks_qsat + feedbacks
                sample_queries_list_to_use = sample_queries_list_qsat + sample_queries_list
            else:
                feedbacks_to_use, sample_queries_list_to_use = feedbacks, sample_queries_list
            
            # Run BC+ Reasoner on main query to get feedback
            main_query_feedback, prog_num = get_feedback_main(prog_wo_query, main_query, maxAdditive_line, update_idx, args)
            
            cplus2asp_feedback_all = ''.join([sample_query + '\n\nCplus2ASP Output:\n\n' + feedback + '\n\n' for sample_query, feedback in zip(sample_queries_list, feedbacks)])
            write_intermediate3(output_path, cplus2asp_feedback_all + '\n\n' + main_query_feedback, 'Sample Queries Cplus2ASP Feedback', 0, 6 + update_idx, 1)

    BC_prog = prog_wo_query + '\n\n' + ('noconcurrency.\n\n' if not args.concurrency else '') + main_query 
    write_intermediate3(output_path, BC_prog, 'BC Program', -1,-1)
    output_status, outs_processed, errs, prog_num = run_cplus2asp(main_query, prog_wo_query, maxAdditive = maxAdditive_line, timeout = 60, concurrency = args.concurrency, incremental_mode = True)
    output_to_save = outs_processed
    write_intermediate3(output_path, output_to_save, 'BC output', -1,-1)
    
    total_tokens = [(tt['prompt_tokens'],tt['completion_tokens']) for tt in total_usage]
    arr = np.array(total_tokens)
    save_cache(prompt_cache, model = model)
    
    
