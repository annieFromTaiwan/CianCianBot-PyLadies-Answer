# encoding: utf-8

from datetime import datetime


class InMemoryFakeDB:

    """
    Following is the recommended data storage format.
    However, you could always design your own format if you want.

        records = {
            "unique_id_xxx": [
                ("user_1", "user_2", 70, "dinner", datetime(2017, 5, 13, 12, 1, 57)),
                ("user_2", "user_1", 70, "dinner", datetime(2017, 5, 13, 17, 22, 6)),
            ],
            "unique_id_yyy": [
                ("user_b", "user_a", 110, "lunch", datetime(2017, 5, 13, 10, 21, 58)),
                ("user_b", "user_a", 90, "dinner", datetime(2017, 5, 13, 16, 53, 21)),
                ("user_c", "user_a", 30, "ps4", datetime(2017, 5, 13, 00, 43, 11)),
            ],
        }

        summary = {
            "unique_id_xxx": {
                ("user1", "user2"): 0,
            }
            "unique_id_yyy": {
                ("user_a", "user_b"): -200,
                ("user_a", "user_c"): -30,
            }
        }

    Notice that, in `summary`,
    before inserting and creating a new instance, the two users' names are sorted.

    """

    records = {}
    summary = {}

    def write(self, unique_id, borrower, owner, money, note):
        # 1. Write these information to `records`.
        if borrower == owner:
            return False
        this_window_records = self.records.setdefault(unique_id, [])
        this_window_records.append((borrower, owner, money, note, datetime.today()))

        # 2. Calculate the latest balance_number, and update the result in `summary`.
        person1, person2 = tuple(sorted((borrower, owner)))
        this_window_summaries = self.summary.setdefault(unique_id, {})
        balance_number = this_window_summaries.setdefault((person1, person2), 0)
        if person1 == borrower:
            balance_number += money
        else:
            balance_number -= money
        this_window_summaries[(person1, person2)] = balance_number

        # 3. Return the latest balance_number
        return (person1, person2, balance_number)

    def get_all_summary(self, unique_id):
        # Return all people pairs' balance number.
        this_window_summaries = self.summary.setdefault(unique_id, {})
        for person_tuple, balance_number in this_window_summaries.items():
            yield (person_tuple[0], person_tuple[1], balance_number)

    def get_recent_records(self, unique_id):
        # Return most recent 5 records.
        this_window_records = self.records.get(unique_id, [])
        return sorted(this_window_records, key=lambda t: t[4], reverse=True)[:5]


import traceback
import sys
class PostgreDB:

    def __init__(self, db_conn):
        self.conn = db_conn
        print("Inside db:")
        print(self.conn)

    def write(self, unique_id, borrower, owner, money, note):
        try:
            self._write_records(unique_id, borrower, owner, money, note)
        except Exception as e:
            print("Error when writing records.")
            traceback.print_exc(file=sys.stdout)
            raise e

        try:
            result = self._write_summary(unique_id, borrower, owner, money)
        except Exception as e:
            print("Error when writing summary.")
            traceback.print_exc(file=sys.stdout)
            raise e

        return result

    def _write_records(self, unique_id, borrower, owner, money, note):
        """
        Append new record to table `records`.
        """
        cur = self.conn.cursor()
        cur.execute(
                # Fill in all the ____s. [TODO]
                "INSERT INTO records (____, ____, ____, ____, ____, ____) VALUES (%s, %s, %s, %s, %s, %s)",
                (unique_id, ____, ____, ____, ____, datetime.today())
                )
        self.conn.commit()
        cur.close()

    def _write_summary(self, unique_id, borrower, owner, money):
        """
        Get `balance_number` from table `summary`.
        Calculate new `balance_number`, write back to table `summary`.
        """
        # Step 0 - Sort names. [TODO]

        # Step 1 - Insert if not exists. Then update new value.
        cur = self.conn.cursor()
        cur.execute(
                # Fill in all the ____s. [TODO]
                "INSERT INTO summary (____, ____, ____, ____) \
                        VALUES (____, ____, ____, ____) \
                        ON CONFLICT (____, ____, ____) DO NOTHING",
                (____, ____, ____, ____)
                )
        cur.execute(
                # Fill in all the ____s. [TODO]
                "UPDATE summary \
                        SET ____ = ____ \
                        WHERE ____ = %s and ____ = %s and ____ = %s \
                        RETURNING balance_number",
                (____, ____, ____, ____)
                )
        self.conn.commit()

        balance_number = cur.fetchone()[0]
        cur.close()

        # Step 2 - return new balance_number and people orders.
        return (person1, person2, balance_number)

    def get_all_summary(self, unique_id):
        cur = self.conn.cursor()
        cur.execute(
                "SELECT ____, ____, ____ FROM ____ WHERE ____ = ____",
                (____, )
                )
        for ____, ____, ____ in cur.fetchall():
            yield (____, ____, ____)
        cur.close()

    def get_recent_records(self, unique_id):
        cur = self.conn.cursor()
        cur.execute(
                "SELECT ____, ____, ____, ____, ____ FROM ____ WHERE ____ ORDER BY ____ DESC LIMIT ____",
                (____, )
                )
        records = cur.fetchall()
        cur.close()
        return records


class DataManager:
    def __init__(self, conn=None):
        if not conn:
            self.db = InMemoryFakeDB()
        else:
            self.db = PostgreDB(conn)

    def write(self, unique_id, borrower, owner, money, note):
        return self.db.write(unique_id, borrower, owner, money, note)

    def get_all_summary(self, unique_id):
        return self.db.get_all_summary(unique_id)

    def get_recent_records(self, unique_id):
        return self.db.get_recent_records(unique_id)
