import random
from subprocess import Popen, PIPE
import sys
import os

def remove_paths(text):
    new_lines = []
    for line in text.split('\n'):
        if '[' in line and '.bc' in line:
            s_idx, e_idx = line.index('['), line.index('.bc')
            new_line = line[:s_idx] + 'temp' + line[e_idx:]
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)

def write_temp_query(query):
    rand_int = random.randint(0,15)
    fname = f'temp_bc+/temp_query{rand_int}.bc'
    f = open(fname, "w") # newline = \n needed, cplus2asp requires LF not CRLF
    f.write(query)
    f.close()
    return rand_int

def cplus2asp_WSL(rand_int, custom_cmd, query_sat, timeout = 60*5, incremental_mode= False):
    lib_path = '/home/a/miniconda3/lib'
    file_path = os.path.join(os.getcwd(),f'temp_bc+/temp_query{rand_int}.bc')
    query_cmd = 'sat' if query_sat else '0'
    #linux_command = f"cplus2asp --language=bc+ --mode=static-auto {file_path} --query={query_cmd} {custom_cmd}"
    running_mode = 'static-auto' if not incremental_mode else 'incremental'
    linux_command = f"cplus2asp --language=bc+ --mode={running_mode} {file_path} --query={query_cmd} {custom_cmd}"

    process = Popen(linux_command, shell=True, stdout=PIPE, stderr=PIPE)
    try:
        stdout, stderr = process.communicate(timeout=timeout) # 2 minute timeout
    except:
        print('timeout')
        stdout = b'TIMEOUT'
        stderr = b''
    
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    if 'cplus2asp: not found' in stderr:
        print(stderr)
        sys.exit()
    return stdout, stderr



def planner_wsl(query, domain, custom_cmd, query_sat=False, concurrency = False, label = 'test', timeout = 60*2, incremental_mode = False):
    
    if ':- query.' in query:
        query = query.replace(':- query.', ':- query\nlabel :: 0.')
    prog = domain + ('\nnoconcurrency.\n' if not concurrency else '')
    
    rand_int = write_temp_query(prog + '\n\n' + query)
    
    outs, errs = cplus2asp_WSL(rand_int, custom_cmd, query_sat, timeout=timeout, incremental_mode = incremental_mode)
    if 'Encountered undeclared identifier' in errs:
        pass#breakpoint()
    if 'ERROR' in errs or 'Error' in errs:
        print(errs)
        return 'FAIL', outs, errs, rand_int
    if outs == 'TIMEOUT':
        return 'TIMEOUT', outs, errs, rand_int
    last_out = outs[outs.rindex('clingo version'):]
    if 'UNSATISFIABLE' in last_out:
        return 'False', outs, errs, rand_int
    elif 'SATISFIABLE' in last_out:
        return 'True', outs, errs, rand_int
    else:
        sys.exit()


def getMaxAdditive(text):
    if 'additiveFluent' not in text:
        return ''
    object_declaration_started = False
    lines = text.split('\n')
    for line in lines:
        if ':- objects' in line:
            object_declaration_started = True
        if ('integer' in line or 'int' in line) and '::' in line and object_declaration_started:
            break
    maxAdditive = line[line.index('..')+2:line.index('::')].strip()
    return f':- maxAdditive :: {maxAdditive}.'


def run_cplus2asp(query, domain, maxAdditive, custom_cmd = '', timeout = 60*2,query_sat=False, concurrency=False, incremental_mode = False):
    
    if 'maxAdditive' not in domain:
        domain = maxAdditive + '\n\n' + domain
    prediction, outs, errs, prog_num = planner_wsl(clean_query(query), domain, custom_cmd, query_sat, concurrency=concurrency, timeout = timeout, incremental_mode = incremental_mode)
    errs = remove_paths(errs) # remove filepaths 
    if 'ERROR' in errs:
        return 'FAIL', outs, errs, prog_num
    if prediction == 'TIMEOUT':
        return prediction, outs, errs, prog_num
    output = outs
    if 'Solving' in output:
        output = output[output.rindex('Solving...'):]
    else:
        output = ''
    return prediction, output, errs, prog_num


def process_errors(err_output):
    
    errs = err_output.split('\n')
    errs_dict = {'undeclared variable':[]}
    err_first = 'undeclared identifier' if 'undeclared identifier' in errs[0] else ''#breakpoint()
    all_undeclared = []
    for idx,err in enumerate(errs):
        errs_dict[idx] = err
        if 'undeclared identifier' in err:
            all_undeclared.append(err)
    if err_first == 'undeclared identifier':
        err_to_use = '\n'.join(all_undeclared)
    else:
        err_to_use = errs_dict[0]
    return err_to_use, errs_dict, err_first, all_undeclared
    
def process_output(output):
    new_lines = []
    for line in output.split('\n'):
        if 'Time' in line or 'Calls' in line:
            pass
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)

def split_prog(prog_all):
    segment_idx = -1
    segments_dict = {i:[] for i in range(3)}
    segments_changed = []
    segment_types = []
    for line in prog_all.split('\n'):
        if 'CHANGED' in line and any([word in line.lower() for word in ['main', 'sample', 'program']]):
            segment_idx+=1
            if 'main' in line.lower():
                segment_types.append('main')
            elif 'sample' in line.lower():
                segment_types.append('sample')
            else:
                segment_types.append('program')
            if 'UNCHANGED' in line:
                segments_changed.append(0)
            else:
                segments_changed.append(1)
            continue
        if segment_idx >=0:
            segments_dict[segment_idx].append(line)
    #breakpoint()
    prog, main_query, sample_queries = ['\n'.join(segments_dict[i]) for i in range(3)]
    segments_ordered = []
    segments_changed_ordered = []
    
    for segment_type_to_match in ['program', 'main', 'sample']:
        segment_type_idx = segment_types.index(segment_type_to_match)
        segments_ordered.append('\n'.join(segments_dict[segment_type_idx]))
        segments_changed_ordered.append(segments_changed[segment_type_idx])
    prog, main_query, sample_queries = segments_ordered
    
    return prog, main_query, sample_queries, segments_changed

def split_sample_queries(sample_queries):
    sample_queries = sample_queries.strip()
    
    segments = []
    current_segment_list = []
    first_segment_reached = False
    
    for line in sample_queries.split('\n'):
        if 'query' in line.lower() and '%' in line and ':-' not in line: # query line start
            first_segment_reached = True
            if len(current_segment_list)!=0:
                segments.append('\n'.join(current_segment_list))
                current_segment_list = [line]
                continue
        if first_segment_reached:
            current_segment_list.append(line)
    segments.append('\n'.join(current_segment_list))
            
    segments = [seg for seg in segments if 'query 0' not in seg.lower() and ':-' in seg] # filter out query 0: query=sat 
    
    sample_queries_list = [sample_query for sample_query in segments if ':-' in sample_query]
    
    sample_queries_list_new = []
    for sample_query in sample_queries_list:
        sample_query_new = []
        query_start_reached = False
        termination_reached = False
        for line in sample_query.split('\n'):
            if not query_start_reached:
                sample_query_new.append(line)
                
                if line.strip()[:2]==':-':
                    query_start_reached = True
                    continue
            else:
                if not termination_reached:
                    sample_query_new.append(line)
                else:
                    pass
                if '.' in line:
                    termination_reached = True
        sample_query_new_string = '\n'.join(sample_query_new)
        if not termination_reached:
            if ';' in sample_query_new_string: # replace last semicolon, since no "." was found
                to_replace_idx = sample_query_new_string.rfind(';')
                sample_query_new_string = sample_query_new_string[:to_replace_idx] + '.'
        sample_queries_list_new.append(sample_query_new_string)
    return sample_queries_list_new

def guess_maxstep(query):
    timestamps = []
    for line in query.split('\n'):
        if line == '':
            continue
        first_part = line.strip().split()[0]
        if first_part[-1]==':':
            first_part_stripped = first_part[:-1].strip()
            if first_part_stripped.isnumeric():
                timestamps.append(int(first_part_stripped))
    if len(timestamps)==0:
        timestamps = [0]
    return max(timestamps) + 1

def clean_signature(text):
    last_line_idx = 0
    backup_last_line_idx = 0
    for idx,line in enumerate(text.split('\n')):
        if '::' in line and not any(word in line for word in ['nonexecutable', 'impossible', ' if ', '&']):
            last_line_idx = idx
        if ':' in line and not any(word in line for word in ['nonexecutable', 'impossible', ' if ', '&']):
            backup_last_line_idx = idx
    
    if last_line_idx == 0:
        last_line_idx = backup_last_line_idx
        
    lines = text.split('\n')
    
    sign_lines = lines[:last_line_idx+1]
    after_sign_lines = lines[last_line_idx + 1:]
    
    first_part = '\n'.join(sign_lines)
    second_part = '\n'.join(after_sign_lines)
    
    segments  = first_part.split(':-')
    sign_segments = segments[1:]
    
    sign_segments_new = []
    for segment in sign_segments:
        if 'sorts' in segment:
            if '.' not in segment:
                lsplit, rsplit = segment.rsplit(';', 1)
                new_segment = ':-' + lsplit + '.' + rsplit
                sign_segments_new.append(new_segment)
            else:
                sign_segments_new.append(':-'+ segment)
            continue
        elif not '::' in segment:
            sign_segments_new.append(':-' + segment)
            continue

        lines_new = []
        lsplit, rsplit = segment.rsplit('::',1)
        
        rsplit = rsplit.replace(';','.')
        
        line_new = ':-' + '::'.join([lsplit, rsplit])
        lines_new.append(line_new)
            
        sign_segments_new.append('\n'.join(lines_new))
    
    return '\n'.join(sign_segments_new) + '\n' +  second_part

def no_action_query(query):

    bc_step = 0
    step_0_lines = []
    for line in query.split('\n'):
        if ': ' in line and '::' not in line and 'maxstep' not in line:
            bc_step = int(line.split(':')[0].strip())
            if bc_step==0:
                step_0_lines.append(line)
            #new_lines.append(f'    {filtered_step}:' + line.split(':')[1])
    
    if len(step_0_lines) == 1:
        pass
    elif len(step_0_lines) >1:
        if step_0_lines[-1].count('&')==0: # step 0 action
            step_0_lines.pop(-1)
    initial_facts = '\n'.join(step_0_lines)
    query_template = f''':- query
    {initial_facts}
        maxstep :: 0.'''
    
    return query_template, initial_facts

def iterate_actions_query(step, orig_query):
    test = orig_query
    action_idx = 0

    query_split = test.split('\n')#test[test.index('query'):].split('\n')
    new_query = ''
    for line in query_split:
        if 'maxstep' in line and '::' in line:
            new_query+= '\n' + f'maxstep :: {action_idx}.'#line
            continue
        elif 'query' in line:
            new_query+='\n' + line
            continue
        elif ':' in line:
            step_num = line[:line.index(':')]
            step_num = step_num.strip()
            line_elements = line[line.index(':'):]
            list_elements = line_elements.split('&')
            if len(list_elements)>1:
                if int(step_num)==0:
                    new_query+= '\n' + line
                else:
                    continue
            elif action_idx <=step:
                if action_idx == int(step_num):
                    new_query += '\n' + line#actions.append(line)
                    action_idx+=1
                else:
                    continue
            else:
                continue
        else:
            new_query+='\n' + line
    
    if ';' in new_query and '.' not in new_query: # replace last semicolon, since no "." was found
        to_replace_idx = new_query.rfind(';')
        new_query = new_query[:to_replace_idx] + '.'
    
    return new_query, action_idx


def iterate_actions(query_w_comment, domain, maxAdditive, return_query=True, timeout = 60*2, query_sat=False):
    current_step = 0
    pre_query, query = query_w_comment.split(':-')
    query = ':-' + query
    orig_query = query
    step_max = max([int(line.split(':')[0].strip()) for line in orig_query.split('\n') if ': ' in line and '::' not in line and 'maxstep' not in line])
    queries = [no_action_query(query)[0]]
    output_status, outs_processed, errs, prog_num = run_cplus2asp(query, domain, maxAdditive, custom_cmd = f'--maxstep 0', timeout = timeout)
    
    outputs_list = [outs_processed]
    
    if output_status == 'False':
        last_sat_step= [line for line in query.split('\n') if f'{current_step}:' in line]
        last_sat_step = ' and '.join(last_sat_step)
        extra_details = failure_feedback_formatter(current_step+1, last_sat_step, queries, outputs_list)
        return  output_status, outs_processed, queries[0], errs, prog_num, extra_details
    
    while current_step < step_max:
        query, current_step = iterate_actions_query(current_step, orig_query)
        sample_maxstep = guess_maxstep(query)
        #query = fix_query(query, preds_to_fix)
        queries.append(query)
        #breakpoint()
        output_status, outs_processed, errs, prog_num = run_cplus2asp(query, domain, maxAdditive, custom_cmd = f'--maxstep {sample_maxstep}', timeout = timeout)
        outputs_list.append(outs_processed)
        if 'unsatis' in outs_processed.lower():
            
            breakpoint() # check the following
            last_sat_step= [line for line in query.split('\n') if f'{current_step-1}:' in line]
            last_sat_step = ' and '.join(last_sat_step)
            extra_details = failure_feedback_formatter(current_step, last_sat_step, queries, outputs_list)
            if return_query==True:
                return output_status, outs_processed, queries[-2], errs, prog_num, extra_details


def failure_feedback_formatter(current_step, last_sat_step, queries, outputs_list):
    # failed query
    
    if len(queries)==1:
        queries = queries + queries
        outputs_list = outputs_list + outputs_list
    feedback = '''
% The query fails!

Each step is satisfiable up until <STEP>, which has state/actions: "<LAST_SAT_STEP>", which should be satisfiable but they are not.

The last satisfiable state, correponding to this query is:
<WORKING_QUERY>

is:

<OUTPUTS_WORKING>

The actions and states are shown up until the last step in the query which is satisfiable. Consider why "<LAST_SAT_STEP>" cannot be executed in step <STEP>. Look at the last satisfiable state in the plan, and the rules which involve or may affect "<LAST_SAT_STEP>", which would cause it to be nonexecutable (if it is an action) or cause something that leads to the query being unsatisfiable.
    '''.replace('<STEP>',str(current_step-1)).replace('<LAST_SAT_STEP>',last_sat_step).replace('<WORKING_QUERY>',queries[-2]).replace('<OUTPUTS_WORKING>',outputs_list[-2])
    
    return feedback

def get_sat_feedback(sat_output, errs):
    #breakpoint()
    sample_queries_list_qsat = []
    feedbacks_sat = []
    if sat_output == 'True': # ignore satisfiable
        sample_queries_list_qsat.insert(0, None)
        feedbacks_sat.insert(0, None)
    elif sat_output == 'FAIL':
        err_to_use, errs_dict, err_first, all_undeclared = process_errors(errs)
        sample_queries_list_qsat.insert(0,'% Query 0: Check satisfiability of program signature and rules (ignores other queries). (satisfiable)\n:- query = sat.')
        feedbacks_sat.insert(0,f'{err_to_use}\n\nSince this fails, check the error message(s).')
    elif sat_output == 'False': #if unsatisfiable, then there is an issue
        sample_queries_list_qsat.insert(0,'% Query 0: Check satisfiability of program signature and rules (ignores other queries). Make sure that the  (satisfiable)\n:- query = sat.')
        feedbacks_sat.insert(0,'Since this fails, this indicates a deeper, high priority issue related to the signature and/or rules. \n* Check the signature, so that fluents can have values that exist given the sorts and objects and that there are no rules which necessarily lead to contradiction. If a constant is declared for example like "fluentName(args) :: inertialFluent(sort);...", where "sort" is a declared sort, then there should be some objects for that sort that are declared. For example, if a constant is declared like "loc(car) :: inertialFluent(location);...", then there should be objects declared of sort "location" (or of a sort which has location as a supersort (location >> otherSort)). Keep in mind that sorts representing integers, should have objects declared which are numbers (e.g., "integer :: 0..5", or "integer :: 0, 1, 2, ..."). Integers should be only up to what is needed, since unnecessarily large numbers will cause the solver to take a long time.\n* Check that there are no simple or rigid fluents of any kind or any nonspecified constant types (they should only be either "exogenousAction" or "inertialFluent"). Instead of rigid or simple fluents, use inertialFluent, even if it is not intuitive.')
    else:
        sample_queries_list_qsat.insert(0,'% Query 0: Check satisfiability of program signature and rules (ignores other queries). (satisfiable)\n:- query = sat.')
        feedbacks_sat.insert(0,'\n\nThe query timed out.')
        #breakpoint()
    return sample_queries_list_qsat, feedbacks_sat

def get_sat_feedback2(sat_output, errs):
    #breakpoint()
    sample_queries_list_qsat = []
    feedbacks_sat = []
    if sat_output == 'True': # ignore satisfiable
        sample_queries_list_qsat.insert(0, None)
        feedbacks_sat.insert(0, None)
        satisfiable = True
    elif sat_output == 'FAIL':
        err_to_use, errs_dict, err_first, all_undeclared = process_errors(errs)
        sample_queries_list_qsat.insert(0,'% Query 0: Check satisfiability of program signature and rules (ignores other queries). (satisfiable)\n:- query = sat.')
        feedbacks_sat.insert(0,f'{err_to_use}\n\nSince this fails, check the error message(s).')
        satisfiable = False
    elif sat_output == 'False': #if unsatisfiable, then there is an issue
        sample_queries_list_qsat.insert(0,'% Query 0: Check satisfiability of program signature and rules (ignores other queries). Make sure that the  (satisfiable)\n:- query = sat.')
        feedbacks_sat.insert(0,'Since this fails, this indicates a deeper, high priority issue related to the signature and/or rules. \n* Check the signature, so that fluents can have values that exist given the sorts and objects and that there are no rules which necessarily lead to contradiction. If a constant is declared for example like "fluentName(args) :: inertialFluent(sort);...", where "sort" is a declared sort, then there should be some objects for that sort that are declared. For example, if a constant is declared like "loc(car) :: inertialFluent(location);...", then there should be objects declared of sort "location" (or of a sort which has location as a supersort (location >> otherSort)). Keep in mind that sorts representing integers, should have objects declared which are numbers (e.g., "integer :: 0..5", or "integer :: 0, 1, 2, ..."). Integers should be only up to what is needed, since unnecessarily large numbers will cause the solver to take a long time.\n* Check that there are no simple or rigid fluents of any kind or any nonspecified constant types (they should only be either "exogenousAction" or "inertialFluent"). Instead of rigid or simple fluents, use inertialFluent, even if it is not intuitive.')
        satisfiable = False
    else:
        sample_queries_list_qsat.insert(0,'% Query 0: Check satisfiability of program signature and rules (ignores other queries). (satisfiable)\n:- query = sat.')
        feedbacks_sat.insert(0,'\n\nThe query timed out.')
        satisfiable = False
        #breakpoint()
    return satisfiable, sample_queries_list_qsat, feedbacks_sat


def clean_query(query):
    new_lines = []
    for line in query.split('\n'):
        if 'label' in line and '::' in line:
            pass
        elif '%' in line:
            if line.strip()[0]=='%':
                pass
        else:
            new_lines.append(line)
    new_query = '\n'.join(new_lines)
    if '.' not in new_query and ';' in query:
        li = new_query.rsplit(';',1)
        new_query = '.'.join(li)
    return new_query

def split_prog_query(text):
    prog_wo = []
    query = []
    query_start = False
    
    for line in text.split('\n'):
        if not query_start:
            if 'query' in line.lower() and line.strip()[0] == '%':
                query_start = True
                query.append(line)
            else:
                prog_wo.append(line)
        else:
            query.append(line)
    
    
    return '\n'.join(prog_wo), '\n'.join(query)
