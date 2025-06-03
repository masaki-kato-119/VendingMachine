class State:
    WAITING = "待機中"
    INSERTING_MONEY = "お金投入"
    SELECTING_PRODUCT = "商品選択中"
    DISPENSING_PRODUCT = "商品払い出し"
    DISPENSING_CHANGE = "釣銭払い出し"
    COMPLETED = "購入完了"




class VendingMachine:
    def __init__(self):
        self.state = State.WAITING  # 初期状態
        
        self.display_panel = DisplayPanel()
        self.product_rack = ProductRack()
        self.money_input = MoneyInput()
        self.change_machine = ChangeMachine()
        self.product_dispenser = ProductDispenser()
        self.sales_vault = SalesVault()
        self.control_panel = ControlPanel()

    def transition_state(self, next_state):
        """ 状態遷移の検証 """
        valid_transitions = {
            State.WAITING: [State.INSERTING_MONEY],
            State.INSERTING_MONEY: [State.SELECTING_PRODUCT],
            State.SELECTING_PRODUCT: [State.DISPENSING_PRODUCT, State.DISPENSING_CHANGE],
            State.DISPENSING_PRODUCT: [State.DISPENSING_CHANGE],
            State.DISPENSING_CHANGE: [State.COMPLETED],
        }

        if next_state in valid_transitions.get(self.state, []):
            print(f"hnote over 自動販売機: {next_state}")
            self.state = next_state
        else:
            print(f"hnote over 自動販売機: {next_state}")

    def sequence_demo(self):
        # 在庫と釣銭確認
        self.transition_state(State.WAITING)
        print('自動販売機 -> ', end='')
        stock = self.product_rack.get_stock_info()

        print('自動販売機 -> ', end='')
        change = self.change_machine.get_current_change()

        print('自動販売機 -> ', end='')
        self.display_panel.display_product_list(stock)
        print('表示パネル -> 利用者 : 商品、価格、在庫有無')

        print('自動販売機 -> ', end='')
        self.display_panel.display_change_status(change)
        print('表示パネル -> 利用者 : 釣銭有無')

        # お金投入
        self.transition_state(State.INSERTING_MONEY)
        print('利用者 -> 投入金口 : お金投入')

        print('自動販売機 -> ', end='')
        money = self.money_input.check_inserted_amount()

        print('自動販売機 -> ', end='')
        self.display_panel.display_total_amount(money)

        print('表示パネル -> 利用者 : 合計投入金額')

        print('自動販売機 -> ', end='')
        self.control_panel.light_selectable_buttons()

        print('操作パネル -> 利用者 : 選択可能な商品ボタン')

        # 商品選択
        self.transition_state(State.SELECTING_PRODUCT)


        print('利用者 -> 操作パネル : 商品ボタン押下')

        print('自動販売機 -> ', end='')
        self.control_panel.check_button_press()

        print('自動販売機 -> ', end='')
        self.product_rack.dispense_product()

        print('自動販売機 -> ', end='')
        self.product_dispenser.receive_product()

        print('商品取り出し口 -> 利用者 : 商品')

        print('自動販売機 -> ', end='')
        self.change_machine.get_current_change()

        # 釣銭払い出し
        self.transition_state(State.DISPENSING_CHANGE)

        print('自動販売機 -> ', end='')
        self.display_panel.guide_change_refund()

        print('表示パネル -> 利用者 : 釣銭_返金の有無')

        print('自動販売機 -> ', end='')
        self.change_machine.dispense_change()

        print('釣銭機 -> 利用者 : 釣銭')

        # 完了
        self.transition_state(State.COMPLETED)

class DisplayPanel:
    def display_product_list(self, stock):
        print(f"表示パネル : 商品一覧_商品名_商品価格_商品在庫有無等_を表示({stock})")

    def display_change_status(self, change):
        print(f'表示パネル : 釣銭有無を表示({change})')

    def guide_change_refund(self):
        print('表示パネル : 釣銭_返金の払い出しを案内')

    def display_notification(self):
        print('表示パネル : 通知なし')

    def display_total_amount(self, money):
        print(f'表示パネル : 合計投入金額を表示({money})')

class ProductRack:
    def get_stock_info(self):
        print('商品ラック : 商品の在庫_情報を取得')
        return '商品在庫情報' 

    def dispense_product(self):
        print('商品ラック : 商品を払い出す')

class MoneyInput:
    def standby(self):
        print('投入金口 : 待機状態になる')

    def check_inserted_amount(self):
        print('投入金口 : 投入された金額を確認')

        print('投入金口 -> ', end='')
        self.recognize_amount()

        print('投入金口 -> ', end='')
        self.get_inserted_amount()

        print('投入金口 -> ', end='')
        self.update_total_amount()

        return '投入金額'

    def recognize_amount(self):
        print('投入金口 : 金額認識')

    def get_inserted_amount(self):
        print('投入金口 : 投入金額を取得')

    def update_total_amount(self):
        print('投入金口 : 合計投入金額を更新')

    def refund(self):
        print('投入金口 : 投入物を返却')

class ChangeMachine:
    def get_current_change(self):
        print('釣銭機 : 現在の釣銭残量を取得する')
        return '釣銭残量'

    def dispense_change(self):
        print('釣銭機 : 釣銭_返金排出口に金額を払い出す')

class ProductDispenser:
    def receive_product(self):
        print('商品取り出し口 : 商品を受け取る')

class SalesVault:
    def store_sales(self):
        print('売上金庫 : 売上金を保管する')

    def collect_sales(self):
        print('売上金庫 : 売上金を回収する')

class ControlPanel:
    def light_selectable_buttons(self):
        print('操作パネル : 選択可能な商品ボタンを点灯')

    def check_button_press(self):
        print('操作パネル : 商品ボタン押下を確認')

    def check_amount_stock_change(self):
        print('操作パネル : 投入金額_商品在庫および釣銭状況を確認')

    def complete_purchase(self):
        print('操作パネル : 購入処理完了')


def main():
    vending_machine = VendingMachine()
    vending_machine.sequence_demo()
    print('finsih!')

if __name__ == "__main__":
    main()