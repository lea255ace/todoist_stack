import os
import argparse
from todoist_api_python.api import TodoistAPI

api = ''
stack_project_name = 'Stack'
stack_project_id = 0

def locate_stack_project():
    try:
        projects = api.get_projects()
    except Exception as error:
        print(error)
        exit(1)

    try:
        stack_project = next((p for p in projects if p.name == stack_project_name))
    except StopIteration as error:
        print('Unable to locate project \'' + stack_project_name + '\'!')
        print('Either create the project or provide an alternate name with the \'-p\' flag.')
        exit(1)
    
    global stack_project_id
    stack_project_id = stack_project.id

def perform_pop_operation():
    filterString = '#' + stack_project_name + ' & !@stackdone'
    try:
        tasks = api.get_tasks(filter=filterString)
    except Exception as error:
        print(error)
        exit(1)

    if (len(tasks) == 0):
        print('No active tasks found on the stack!')
        exit(0)

    top_task = max(tasks, key=lambda task: task.created_at)
    top_task.labels.append('stackdone')

    try:
        api.update_task(task_id=top_task.id, labels=top_task.labels)
    except Exception as error:
        print(error)
        exit(1)

    print('Popped task \''+ top_task.content + '\' off of the stack.')

def perform_push_operation(description):
    try:
        api.add_task(content=description, project_id=stack_project_id)
    except Exception as error:
        print(error)
        exit(1)

    print('Pushed task \'' + description + '\' onto the stack.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key_file',
                        help='NOT IMPLEMENTED! \
                            Filename from which to read the API key. \
                            If not provided, key will be read from TODOIST_API_KEY environment variable')
    parser.add_argument('-i', '--proj_id',
                        help='Directly provide the project id to skip the project lookup step.')
    parser.add_argument('-n', '--proj_name',
                        help='Optionally override the default project name \'Stack\'. \
                            This option will be ignored if a project ID is supplied with the \'-i\' flag.')
    subparsers = parser.add_subparsers(dest='operation')
    subparsers.required = True

    push_helpstring='Push an item onto the stack'
    parser_push = subparsers.add_parser('push', help=push_helpstring, description=push_helpstring)
    parser_push.add_argument('desc', help='Item description')

    pop_helpstring = 'Pop the newest item off of the stack'
    parser_pop = subparsers.add_parser('pop', help=pop_helpstring, description=pop_helpstring)

    args = parser.parse_args()

    if (args.key_file):
        # TODO(MW): Read API key from provided file
        print('not yet implemented')
    elif (os.environ.get('TODOIST_API_KEY') != None): 
        api_key = os.environ['TODOIST_API_KEY']
    else:
        print('Error: No API key provided.' + '\n')
        parser.print_usage()
        print('\n')
        exit(1)

    api = TodoistAPI(api_key)

    if (args.proj_id):
        stack_project_id = args.proj_id
    else:
        if (args.proj_name):
            stack_project_name = args.proj_name
        locate_stack_project()

    if (args.operation == 'pop'):
        perform_pop_operation()
    else:
        perform_push_operation(args.desc)