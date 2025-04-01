from datetime import datetime

import flask
import json

from main import get_table, add_driver_customer

app = flask.Flask(__name__)


class SumRequest:
    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2



class Request:
    def __init__(self, table_name):
        self.table_name = table_name


class SumResponse:
    def __init__(self, s):
        self.s = s

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class GetResponse:
    def __init__(self, s):
        self.s = s

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class PostResponseDriverCustomer:
    def __init__(self, who, first_name, second_name):
        self.who = who
        self.first_name = first_name
        self.second_name = second_name


class NewResp:
    def __init__(self, s):
        self.s = s

    def toJson(self):
        return json.dumps(self, default=self.custom_serializer)

    @staticmethod
    def custom_serializer(o):
        if isinstance(o, datetime):
            return o.isoformat()  # Преобразуем datetime в строку
        return o.__dict__  # Для остальных объектов используем __dict__


@app.route("/sum", methods=["POST"])
def handle():
    data = flask.request.get_json()

    req = Request(**data)
    resp = SumResponse(req.s1 + req.s2)

    return resp.toJson(), 200


@app.route("/getTable", methods=["GET"])
def request_table():
    try:
        table_name = flask.request.args.get("table_id")

        response = NewResp(get_table(table_name))

        return response.toJson(), 200
    except Exception as e:
        return f"Error: {e}"


@app.route("/addDriverOrCustomer", methods=["POST"])
def request_add_driver_customer():
    data = flask.request.get_json()
    who = PostResponseDriverCustomer(**data).who
    first_name = PostResponseDriverCustomer(**data).first_name
    second_name = PostResponseDriverCustomer(**data).second_name

    result = NewResp(add_driver_customer(who, first_name, second_name))

    return result.toJson()


if __name__ == '__main__':
    app.run('0.0.0.0', port=9000)
    print(request_add_driver_customer)
