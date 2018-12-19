from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

TODOS = {
    '1': {'task': 'build an API'},
    '2': {'task': '?????'},
    '3': {'task': 'profit!'},
}

DONES = {
}

def abort_if_list_doesnt_contain_id(l, i):
    if i not in l:
        abort(404, message="Todo {} doesn't exist".format(i))

parser = reqparse.RequestParser()
parser.add_argument('task')
parser.add_argument('status')

# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_list_doesnt_contain_id(TODOS, todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_list_doesnt_contain_id(TODOS, todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys())) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

class TodoStatus(Resource):
    def put(self, todo_id):
        abort_if_list_doesnt_contain_id(TODOS, todo_id)
        args = parser.parse_args()
        if args['status'] == 'done':
            DONES[todo_id] = TODOS[todo_id]
            del TODOS[todo_id]
        return DONES[todo_id], 201

class Done(Resource):
    def get(self, done_id):
        abort_if_list_doesnt_contain_id(DONES, done_id)
        return DONES[done_id]

    def delete(self, done_id):
        abort_if_todo_doesnt_exist(DONES, done_id)
        del DONES[done_id]
        return '', 204


class DoneList(Resource):
    def get(self):
        return DONES
    # def put(self, done_id):
    #     args = parser.parse_args()
    #     task = {'task': args['task']}
    #     DONES[done_id] = task
    #     return task, 201


##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')

api.add_resource(TodoStatus, '/todos/<todo_id>/status')
api.add_resource(Done, '/dones/<done_id>')
api.add_resource(DoneList, '/dones/')

if __name__ == '__main__':
    app.run(debug=True)