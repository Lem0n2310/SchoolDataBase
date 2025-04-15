from datetime import datetime

import flask
import json

from main import get_table, add_driver_customer, add_order, update_order, delete_record

app = flask.Flask(__name__)


class UpdateRequest:
    def __init__(self, order_id, status):
        self.order_id = order_id
        self.status = status


class DeleteReq:
    def __init__(self, table, id):
        self.table = table
        self.id = id


class Request:
    def __init__(self, table_name):
        self.table_name = table_name


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


class PostResponseOrder:
    def __init__(self,
                 start_destination,
                 end_destination,
                 order_time,
                 car_number,
                 driver_id,
                 customer_id,
                 status,
                 ):
        self.start_destination = start_destination
        self.end_destination = end_destination
        self.order_time = order_time
        self.car_number = car_number
        self.driver_id = driver_id
        self.customer_id = customer_id
        self.status = status


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


@app.route("/addOrder", methods=["POST"])
def request_add_order():
    data = flask.request.get_json()
    start_destination = PostResponseOrder(**data).start_destination
    end_destination = PostResponseOrder(**data).end_destination
    order_time = PostResponseOrder(**data).order_time
    car_number = PostResponseOrder(**data).car_number
    driver_id = PostResponseOrder(**data).driver_id
    customer_id = PostResponseOrder(**data).customer_id
    status = PostResponseOrder(**data).status

    result = NewResp(add_order(
        start_destination,
        end_destination,
        order_time,
        car_number,
        driver_id,
        customer_id,
        status
    ))

    return result.toJson()


@app.route("/updateOrderStatus", methods=["PUT"])
def request_update_order():
    data = flask.request.get_json()
    order_id = UpdateRequest(**data).order_id
    new_status = UpdateRequest(**data).status

    result = NewResp(update_order(order_id, new_status))

    return result.toJson()


@app.route("/delete", methods=["DELETE"])
def request_delete():
    data = flask.request.get_json()
    table = DeleteReq(**data).table
    id = DeleteReq(**data).id

    result = NewResp(delete_record(table, id))

    return result.toJson()


if __name__ == '__main__':
    app.run('0.0.0.0', port=9000)
    print(request_delete)
