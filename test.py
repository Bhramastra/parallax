import px

px.init()
px.deploy("test.txt")
task_id=px.execute("ga","dsd")
while 1:
    print px.fetch(task_id)