# encoding: utf-8

import re

class CianCianBot:
    commands = {
            "HELP": ("說明", "幫幫"),
            "SUMMARY": (),  # [TODO 8]
            "RECENT_RECORDS": (),  # [TODO 10]
            "INTERNAL_TEST": ("測試帳號",),
            }

    def __init__(self, data_manager):
        self.data_manager = data_manager

    def get_help(self):
        """
        Returns a string to help new users.
        """
        # [TODO 1]
        help_msg = "讓我來教你要怎麼使用小茜茜！"



        return help_msg

    @staticmethod
    def _get_presenting_order(person1, person2, balance_number):
        """
        Sort the presenting order of the two people.

        Returns:
            (borrower, owner, money)
            Where `money` should be positive.
        """
        # [TODO 6]
        # case 1 -「B欠A $xx元」, xx > 0


        # case 2 -「A欠B $xx元」, xx > 0



        return (person1, person2, balance_number)

    def get_summary(self, unique_id):
        '''
        Get balance number from all pairs in the database.
        '''
        # 1. Get balance records from database [TODO 8]



        # 2. Format outputs
        #    "目前 熊大欠茜茜 5566元，茜茜欠大雄 1234元，大雄欠熊大 888元。"
        strs = []
        for person1, person2, balance_number in balance_records:
            strs.append("%s欠%s %d元" % self._get_presenting_order(person1, person2, balance_number))
        main_sentences = "，".join(strs)
        if not main_sentences:
            return "目前沒有任何記錄哦！！"
        else:
            return "目前 " + main_sentences + "。"

    def get_recent_records(self, unique_id):
        try:
            records = self.data_manager.get_recent_records(unique_id)
        except Exception:
            return "抱歉，擷取資料時出現了錯誤。"

        if not records:
            return "目前沒有任何記錄哦！"

        # Formating records to strings. [TODO 12]
        #
        # ------ Example ------
        # 2016/1/3 14:23
        # 熊大欠茜茜 300元 午餐吃了超好吃的雅室牛排
        #
        # 2016/1/4 19:23
        # 熊大欠茜茜 1490元 神魔卡包
        # ---------------------

        result = str(records)
        return result

    def process_borrow_statement(self, msg, unique_id):
        """
        If `msg` is not a borrow statement, return None.
        Otherwise, return the result of writing this borrow record.

        Returns:
            A string, that shows
            1. The result of writing borrow record.
            2. Current balance number between the two people mentioned.

            Or when encountering an error, returns a string indicating the error.
        """
        match_obj = re.match("[TODO 2]", msg)
        if not match_obj:
            return None

        # 1. Extract `borrower`, `owner`, `money`, `note` from `msg`. [TODO 3]


        # 2. Write the record (`borrower`, `owner`, `money`, `note`) to DataManager.
        #    Hint: call `self.data_manager.write(...)`
        #    [TODO 4]



        # 3. Return the result of this record. [TODO 3],
        #    also returns the latest balance_number. [TODO 4]
        #    Hint: Use `self._get_presenting_order(...)` after finish [TODO 6]


        return "已紀錄 熊大欠茜茜 20元。\n目前 茜茜欠熊大 180元。"

    def respond(self, msg, unique_id):
        """
        The main responding mechanism of CianCianBot.

        Args:
            msg: User's message.
            unique_id: The chatting window id of that user.

        Returns:
            A string.
        """

        # 「說明、幫幫」
        if msg in self.commands["HELP"]:
            return self.get_help()

        # 「結帳」Use `self.get_summary(...)` [TODO 8]


        # 「最近帳單」Use `self.get_recent_records(...)` [TODO 10]


        # 「測試帳號」(Only for testing)
        elif msg in self.commands["INTERNAL_TEST"]:
            return unique_id

        else:
            result = self.process_borrow_statement(msg, unique_id)
            if not result:
                return "我聽不懂你在說什麼！"
            else:
                # 「A欠B $$$元」
                return result


if __name__ == "__main__":

    ##########################################
    # A function for local test.
    ##########################################

    def local_test(msg, bot):
        if msg:
            bot_response = bot.respond(msg, "fake_unique_id_for_testing")
            print("-" * 30)
            print("  [User]")
            print(msg)
            print("  [Bot]")
            print(bot_response)
        else:
            # If `msg` is None, print newlines, forming a paragraph.
            print("\n\n")

    ##########################################
    # Basic testcases.
    ##########################################

    testcases = [
            "說明",
            "結帳",
            "結帳RRRR",
            "最近帳單",
            None,

            "茜茜欠熊大300元",
            "茜茜欠熊大300元吃晚餐",
            "茜茜 欠 熊大 300元 吃晚餐",
            "熊大 欠 茜茜 999元 還錢",
            None,

            "大雄欠大雄1234元咖啡店",
            None,

            "茜茜朋友欠茜茜120元咖啡店",
            "茜茜 欠 熊大 44元 熊大還錢給茜茜了",
            None,

            "我欠5566 5566元 五六不能亡！",
            "5566欠我 5566元 五六不能亡！",
            None,

            "你好笨",
            None,

            "結帳",
            "最近帳單",
            "說明",
            ]

    from DataManager import DataManager
    data_manager = DataManager()
    cian_cian = CianCianBot(data_manager)

    for user_input in testcases:
        local_test(user_input, cian_cian)
