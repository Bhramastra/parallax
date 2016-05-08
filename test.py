import px

px.deploy("test.txt")
task_id=px.execute("ga","dsd")
# while px.fetch(task_id):
#     print px.partial(task_id)