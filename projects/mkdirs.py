import os

paths = [
    "projects/antlr4-4.11.0",
    "projects/dbeaver-22.2.5",
    "projects/elasticsearch-8.5.2",
    "projects/exoplayer-2.18.2",
    "projects/fastjson-1.2.83",
    "projects/flink-1.15.3",
    "projects/guava-31.1",
    "projects/jenkins-2.379",
    "projects/libgdx-1.11.0",
    "projects/logstash-8.5.2",
    "projects/mockito-4.9.0",
    "projects/openrefine-3.6.2",
    "projects/presto-0.278",
    "projects/quarkus-2.14.0",
    "projects/questdb-6.6",
    "projects/redisson-3.18.1",
    "projects/rxjava-3.1.5",
    "projects/tink-1.7.0"
]

for path in paths:
    if not os.path.exists(path):
        print(f"Path '{path}' does not exist.")

os.makedirs('../code snippets-without-labels/file/', exist_ok=True)
os.makedirs('../code snippets-without-labels/class/', exist_ok=True)
os.makedirs('../code snippets-without-labels/method/', exist_ok=True)
os.makedirs('../code snippets-without-labels/block/', exist_ok=True)

os.makedirs('../comments-without-labels/all/', exist_ok=True)
os.makedirs('../comments-without-labels/file/', exist_ok=True)
os.makedirs('../comments-without-labels/class/', exist_ok=True)
os.makedirs('../comments-without-labels/method/', exist_ok=True)
os.makedirs('../comments-without-labels/block/', exist_ok=True)

os.makedirs('../comments-with-labels/GGSATD/', exist_ok=True)
os.makedirs('../comments-with-labels/MAT/', exist_ok=True)
os.makedirs('../comments-with-labels/XGBoost/', exist_ok=True)
os.makedirs('../comments-with-labels/Final/', exist_ok=True)

os.makedirs('../comments-with-labels-checked/Final/', exist_ok=True)

os.makedirs('../code snippets-with-labels/file/', exist_ok=True)
os.makedirs('../code snippets-with-labels/class/', exist_ok=True)
os.makedirs('../code snippets-with-labels/method/', exist_ok=True)
os.makedirs('../code snippets-with-labels/block/', exist_ok=True)

os.makedirs('../metrics/', exist_ok=True)

os.makedirs('../code snippets-with-labels&metrics/file/', exist_ok=True)
os.makedirs('../code snippets-with-labels&metrics/class/', exist_ok=True)
os.makedirs('../code snippets-with-labels&metrics/method/', exist_ok=True)
os.makedirs('../code snippets-with-labels&metrics/block/', exist_ok=True)