import ast


def json_txt():
    f = open("test.json")
    data = ast.literal_eval(f.read())
    print(data["meals"][0]["strMeal"])


if __name__ == "__main__":
    json_txt()