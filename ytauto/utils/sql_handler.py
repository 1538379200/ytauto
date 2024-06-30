import psycopg2
from pathlib import Path
import toml


class SqlHandler:
    def __init__(self):
        file = Path(__file__).resolve().parents[1] / "config" / "sql.toml"
        data = toml.load(file)
        self.conn = psycopg2.connect(
            host=data["sql"]["host"],
            port=data["sql"]["port"],
            user=data["sql"]["username"],
            password=data["sql"]["password"],
            dbname=data["sql"]["dbname"]
        )
        self.cursor = self.conn.cursor()

    def insert_running_device(self, device: str, status: int = -1) -> bool:
        try:
            self.cursor.execute(f"insert into running_status (device, status) values ('{device}', {status});")
            return True
        except Exception:
            return False
        finally:
            self.conn.commit()

    def change_running(self, device: str, status: int, remarks: str = "") -> bool:
        try:
            self.cursor.execute(f"update running_status set status = {status}, remarks = '{remarks}' where device = '{device}';")
            return True
        except Exception:
            return False
        finally:
            self.conn.commit()


sql = SqlHandler()


# if __name__ == "__main__":
#     sql = SqlHandler()
#     # result = sql.insert_running_device("192.168.14.116")
#     # print(result)
#     result = sql.change_running_status("192.168.14.116", status=0)
#     print(result)



