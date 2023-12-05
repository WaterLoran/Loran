import yaml


def read_config():
    with open("./environment.yaml", 'r', encoding='utf-8') as f:
        env_res = yaml.load(f.read(), Loader=yaml.FullLoader)
    print("env_res", env_res)
    return env_res

read_config()

