import openai
import time
import pickle
import os

from utils_cplus2asp import split_prog_query, clean_signature, clean_query, split_sample_queries, split_prog
from utils_cplus2asp import getMaxAdditive, run_cplus2asp, process_errors,get_sat_feedback2, guess_maxstep, iterate_actions, process_output


def get_response(prompt, prompt_cache, model, redo=False, temp=0.,max_tokens=3500, stop = None):
    if prompt in prompt_cache and not redo:
        return prompt_cache[prompt], prompt_cache
    
    else:
        passed = False; tries = 0 
        messages = [{'role': 'user', 'content': prompt}]
        while not passed:
            try:
                if model not in ['o1-preview', 'o3-mini', 'o1']:
                    response = openai.ChatCompletion.create(
                        messages=messages,
                        model=model,
                        temperature=0,
                        stop = stop)
                else:
                    response = openai.ChatCompletion.create(
                        messages=messages,
                        model=model)
                    
                passed=True;tries+=1
                prompt_cache[prompt] = response
            except BaseException as e:
                print(e)
                import  sys
                sys.exit()
        return response, prompt_cache

def get_response_check(prompt, prompt_cache, model = 'gpt-4', temp=0,max_tokens=3500, redo=False, stop = None):

    response, prompt_cache = get_response(prompt, prompt_cache, model, redo, temp=temp,max_tokens=max_tokens, stop = stop)
    return response, prompt_cache

def save_cache_basic(prompt_cache, model = 'gpt-4'):
    with open(f'prompt_cache_{model}.pickle', 'wb') as handle:
        pickle.dump(prompt_cache, handle, protocol=pickle.HIGHEST_PROTOCOL)

def save_cache(prompt_cache, model = 'gpt-4'):
    try:
        if os.path.exists(f'prompt_cache_{model}.pickle'):
            with open(f'prompt_cache_{model}.pickle', 'rb') as handle: # load in case it was updated
                temp_prompt_cache = pickle.load(handle)
        else:
            save_cache_basic(prompt_cache, model)
            return
    except:
        breakpoint()
    
    prompt_cache.update(temp_prompt_cache) # combine dicts
    save_cache_basic(prompt_cache, model)

def read_env2(task_name, with_query = False):
    
    desc_file = os.path.join('envs',task_name,'prob_desc.txt')
    sign_desc_file = os.path.join('envs',task_name,'signature.txt')
    query_file = os.path.join('envs',task_name,'query.txt')
    
    desc_file = os.path.abspath(desc_file)
    sign_desc_file = os.path.abspath(sign_desc_file)
    f = open(desc_file, "r",encoding = 'utf-8')
    desc = f.read()
    f.close()
    
    f = open(sign_desc_file, "r")
    sig_desc = f.read()
    f.close()
    
    query= ''
    if with_query:
        f = open(query_file, "r")
        query = f.read()
    return desc, sig_desc, query

    
def write_intermediate3(output_dir, output, step,outer_lvl, inner_lvl, inner_inner_level = None):
    #output_dir = os.path.join(output_dir2,output_dir)
    if inner_inner_level is not None:
        inner_inner_level = f'.{str(inner_inner_level)}'
    else:
        inner_inner_level = ''
    if step.lower() == 'bc program' or step.lower() == 'bc output':
        path = os.path.join(output_dir, '100 ' + step + '.txt')
    elif step.lower() == 'asp program':
        path = os.path.join(output_dir, '200 ' + step + '.txt')
    else:
        if outer_lvl==0:
            if inner_lvl == -1:
                path = os.path.join(output_dir,'0 ' + step+f'.txt')
            else:
                path = os.path.join(output_dir,f'0.{inner_lvl}{inner_inner_level} ' + step+f'.txt')
        else:
            path = os.path.join(output_dir,f'{outer_lvl}.{inner_lvl}{inner_inner_level} ' + step+f'.txt')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f'Step: {step}\nFile: {path}')
    return

def extract_signature2(text):
    
    split_idx = text.lower().index('bc+ signature:')
    
    actions_constants = text[:split_idx].strip('```').strip()
    bc_sign = text[split_idx:].strip('```').strip()
    
    return actions_constants, bc_sign


def process_hint(text):
    text = text.replace('of things', 'of objects')
    fluent_pass,action_pass = 0,0
    
    new_text_list = []
    for segment in text.split('\n\n'):
        if 'fluents' in segment.lower():
            fluent_pass+=1
            pass
        else:
            if 'actions' in segment.lower():
                
                new_segment_list = []
                for line in segment.split('\n'):
                    if 'attribute' in line.lower():
                        pass
                    else:
                        new_segment_list.append(line)
                new_segment= '\n'.join(new_segment_list)
                action_pass+=1
                new_text_list.append(new_segment.replace('(','').replace(')',''))
            else:
                new_text_list.append(segment)
    return '\n\n'.join(new_text_list)


def LLM(prompt, step, model, update_idx, prompt_cache, total_usage, paths):
    inputs_path, input_prompts_path, output_path = paths
    if step == 'signature generation':
        
        response, prompt_cache = get_response_check(prompt, prompt_cache, model = model, redo=False)
        response_text_generated_constants = response['choices'][0]['message']['content']
        total_usage.append(response['usage'])
        
        actions_constants, domain = extract_signature2(response_text_generated_constants)
        
        save_cache(prompt_cache, model = model)
            
        write_intermediate3(input_prompts_path, prompt, 'Signature Generation', 0,1)
        write_intermediate3(output_path, domain, 'Signature Generation isolated', 0,1)
        write_intermediate3(output_path, response_text_generated_constants, 'Signature Generation OUTPUT', 0,1)
        return [domain, actions_constants], prompt_cache, total_usage
    
    elif step == 'knowledge generation':
        
        response, prompt_cache = get_response_check(prompt, prompt_cache, model = model, redo=False)
        total_usage.append(response['usage'])
        knowledge_regenerated = response['choices'][0]['message']['content'].replace('```','').strip()
        #knowledge_regenerated = knowledge_regenerated.replace('% generated knowledge','')
        if len(knowledge_regenerated.split('\n')[0].split()) < 4:
            knowledge_regenerated = '\n'.join(knowledge_regenerated.split('\n')[1:])
        save_cache(prompt_cache, model = model)
        knowledge = knowledge_regenerated
            
        write_intermediate3(input_prompts_path, prompt, 'Knowledge Generation', 0,2)
        write_intermediate3(output_path, knowledge, 'Knowledge Generation OUTPUT', 0,2)
            
        knowledge_formatted = '\n'.join([sent for sent in knowledge.split('\n') if (len(sent)!=0 and sent[0]=='%')])
            
        return [knowledge], prompt_cache, total_usage
    elif step == 'rule and query generation':
        response, prompt_cache = get_response_check(prompt, prompt_cache, model = model, max_tokens = 2000, redo=False)
        total_usage.append(response['usage'])
        nl2bc_output = response['choices'][0]['message']['content']
        nl2bc_output = nl2bc_output.replace('```','').strip()

        split_line_idx = [idx for idx, line in enumerate(nl2bc_output.split('\n')) if 'query' in line][0]
        
        bc_constraints = '\n'.join(nl2bc_output.split('\n')[:split_line_idx])
        query_bc = '\n'.join(nl2bc_output.split('\n')[split_line_idx:])
        
        write_intermediate3(input_prompts_path, prompt, 'Rule-Query Generation', 0, 3)
        write_intermediate3(output_path, nl2bc_output, 'Rule-Query Generation OUTPUT', 0, 3)
        
        save_cache(prompt_cache, model = model)
        return [bc_constraints, query_bc], prompt_cache, total_usage
    elif step == 'satisfiability check':
        response, prompt_cache = get_response_check(prompt, prompt_cache, model = model, redo=False)
        total_usage.append(response['usage'])
        raw_output = response['choices'][0]['message']['content']
        
        write_intermediate3(input_prompts_path, prompt, 'Satisfiability Check Program Revision', 0, 5 + update_idx)
        
        if '```' in raw_output:
            if raw_output.count('```')<=2:
                backtick_splits = raw_output.split('```')
                prog_w_query = raw_output.split('```')[1]
            else:
                prog_w_query = '\n'.join(raw_output.split('```')[1:-1]).replace('```','')
        else:
            prog_w_query =raw_output.replace('```','').strip()
        
        write_intermediate3(output_path, prog_w_query, 'Satisfiability Check Program Revision OUTPUT', 0, 5 + update_idx, 2)
        
        prog_wo_query, query_bc = split_prog_query(prog_w_query)
        
        prog_wo_query = clean_signature(prog_wo_query)
        query_bc = "% Main" + query_bc
        query_bc = clean_query(query_bc)
        main_query = query_bc
        update_idx+=1
        save_cache(prompt_cache, model = model)
        return [prog_wo_query, main_query], update_idx, prompt_cache, total_usage
    elif step == 'sample query generation':
        response, prompt_cache = get_response_check(prompt, prompt_cache, model = model, redo=False)
        total_usage.append(response['usage'])
        response_text = response['choices'][0]['message']['content'].replace('```','').strip()
        sample_queries = response_text.replace('```','')
        save_cache(prompt_cache, model = model)
        
        sample_queries_list = split_sample_queries(sample_queries)
        
        write_intermediate3(input_prompts_path, prompt, 'Sample Query Generation', 0, 5 + update_idx)
        write_intermediate3(output_path, sample_queries, 'Sample Query Generation', 0, 5 + update_idx)
        
        return [sample_queries_list], update_idx, prompt_cache, total_usage
    elif step == 'sample and main query feedback':
    
        response, prompt_cache = get_response_check(prompt, prompt_cache, model = model, redo=False)
        total_usage.append(response['usage'])
        updated_prog = response['choices'][0]['message']['content'].replace('```','').strip()
        
        prog_wo_query, main_query, sample_queries, segments_changed = split_prog(updated_prog)
        prog_wo_query = clean_signature(prog_wo_query)

        sample_queries = '% Query 1' + sample_queries.split('% Query 1')[-1]
        sample_queries_list = split_sample_queries(sample_queries)
        
        write_intermediate3(input_prompts_path, prompt, 'Sample + Main Query Program Revision', 0, 6 + update_idx)
        write_intermediate3(output_path, updated_prog, 'Sample + Main Query Program Revision OUTPUT', 0, 6 + update_idx, 2)
        save_cache(prompt_cache, model = model)
        update_idx+=1
        
        return [prog_wo_query, main_query, sample_queries, sample_queries_list], segments_changed, update_idx, prompt_cache, total_usage


def create_output_directory(model, args):

    output_path_base = f'{model}_outputs'
    inputs_path = os.path.join(output_path_base, args.o, 'inputs')
    input_prompts_path = os.path.join(output_path_base, args.o, 'input_prompts')
    output_path = os.path.join(output_path_base,args.o, 'outputs')
    
    os.makedirs(output_path_base, exist_ok=True)
    os.makedirs(inputs_path, exist_ok=True)
    os.makedirs(input_prompts_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)
    
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    if not os.path.exists(input_prompts_path):
        os.mkdir(input_prompts_path)
    if not os.path.exists('temp_bc+'):
        os.mkdir('temp_bc+')
    return inputs_path, output_path, input_prompts_path


def satisfiability_check(prog_wo_query, args):
    maxAdditive_line = getMaxAdditive(prog_wo_query) if not args.maxAdditive else f':- maxAdditive :: {args.maxAdditive}.'
    sat_output, output, errs, prog_num = run_cplus2asp('', prog_wo_query, maxAdditive = maxAdditive_line, custom_cmd= '', timeout = 60, query_sat=True, concurrency = args.concurrency)
    err_to_use, errs_dict, err_first, all_undeclared = process_errors(errs)
    satisfiable, sample_queries_list_qsat, feedbacks_qsat = get_sat_feedback2(sat_output, errs)
    
    return sat_output, satisfiable, errs, sample_queries_list_qsat, feedbacks_qsat, prog_num


def get_feedback(sample_query, prog_wo_query, args):
    if '(unsatisfiable)'in sample_query:
        query_expected = 'unsat'
    else:
        query_expected = 'sat'
    extra_details = ''
    sample_maxstep = guess_maxstep(sample_query)
    maxAdditive_line = getMaxAdditive(prog_wo_query) if not args.maxAdditive else f':- maxAdditive :: {args.maxAdditive}.'
    output_status, output, errs, prog_num = run_cplus2asp(sample_query, prog_wo_query, maxAdditive = maxAdditive_line, custom_cmd= f'--maxstep {sample_maxstep}', timeout = 60, concurrency = args.concurrency)
    if query_expected == 'sat' and output_status == 'False' and sample_maxstep>1: # query expected to be satisfiable is not, therefore, iteratively run for each timestep up until last executable timestep
        output_status, outs_processed, last_query, errs, prog_num, extra_details = iterate_actions(sample_query, prog_wo_query, maxAdditive = maxAdditive_line)
    if 'ERROR' in errs:
        err_to_use, errs_dict, err_first, all_undeclared = process_errors(errs)
        
        feedback = err_to_use
    else:
        if output_status == 'TIMEOUT':
            feedback = output_status
        else:
            feedback = process_output(output)
    
    return feedback, extra_details, maxAdditive_line

def get_feedback2(sample_query, prog_wo_query, args):
    if '(unsatisfiable)'in sample_query:
        query_expected = 'unsat'
    else:
        query_expected = 'sat'
    extra_details = ''
    sample_maxstep = guess_maxstep(sample_query)
    maxAdditive_line = getMaxAdditive(prog_wo_query) if not args.maxAdditive else f':- maxAdditive :: {args.maxAdditive}.'
    output_status, output, errs, prog_num = run_cplus2asp(sample_query, prog_wo_query, maxAdditive = maxAdditive_line, custom_cmd= f'--maxstep {sample_maxstep}', timeout = 60, concurrency = args.concurrency)
    if query_expected == 'sat' and output_status == 'False' and sample_maxstep>1: # query expected to be satisfiable is not, therefore, iteratively run for each timestep up until last executable timestep
        output_status, outs_processed, last_query, errs, prog_num, extra_details = iterate_actions(sample_query, prog_wo_query, maxAdditive = maxAdditive_line)
    if 'ERROR' in errs:
        err_to_use, errs_dict, err_first, all_undeclared = process_errors(errs)
        
        feedback = err_to_use
    else:
        if output_status == 'TIMEOUT':
            feedback = output_status
        else:
            feedback = process_output(output + extra_details)
    
    return feedback, extra_details, maxAdditive_line

def get_feedback_main(prog_wo_query, main_query, maxAdditive_line, update_idx, args):
    output_status, output, errs, prog_num = run_cplus2asp(main_query, prog_wo_query, maxAdditive = maxAdditive_line, custom_cmd= f'--maxstep {args.main_query_max_step}', timeout = 60, concurrency = args.concurrency, incremental_mode = True)
    
    if 'ERROR' in errs:
        err_to_use, errs_dict, err_first, all_undeclared = process_errors(errs)
        feedback = err_to_use
    else:
            if output_status == 'TIMEOUT':
                feedback = output_status
            else:
                feedback = process_output(output)
    main_query_feedback = main_query + '\n\nCplus2ASP Output:\n\n' + feedback + '\n'

    return main_query_feedback, prog_num
