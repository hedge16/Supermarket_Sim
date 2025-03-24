import sys
import struct
import socket
import time
from PyQt5.QtWidgets import QApplication, QDialog, QLabel
from PyQt5.QtCore import QThread, pyqtSignal, QObject

from client_ui import Ui_Dialog  # UI principale
from cart import Ui_Dialog as Ui_CartDialog  # UI del carrello (rinominata)


class WaitingWindow(QDialog):
    def __init__(self, cliente_id, sock, parent=None):
        super().__init__(parent)
        self.cliente_id = cliente_id
        self.sock = sock
        self.setWindowTitle(f"Cliente {cliente_id} in attesa")
        self.setGeometry(100, 100, 300, 100)
        self.label = QLabel("Attendere prego...", self)
        self.label.setGeometry(50, 40, 200, 20)
        self.waiting_thread = WaitingThread(cliente_id, sock)
        self.waiting_thread.ok_received.connect(self.show_cart_window)
        self.waiting_thread.start()

    def show_cart_window(self):
        self.cart_window = CartWindow(self.cliente_id, self.sock)
        self.cart_window.show()
        self.close()

class WaitingThread(QThread):
    ok_received = pyqtSignal()

    def __init__(self, cliente_id, sock):
        super().__init__()
        self.cliente_id = cliente_id
        self.sock = sock

    def run(self):
        while True:
            response = self.sock.recv(4).decode('utf-8')
            if response == "OK":
                self.ok_received.emit()
                break
            time.sleep(1)

class CartWindow(QDialog, Ui_CartDialog):
    cart_closed = pyqtSignal(int, list, int)

    def __init__(self, cliente_id, sock, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept_cart)
        self.buttonBox.rejected.connect(self.reject_cart)

        self.cliente_id = cliente_id
        self.sock = sock
        self.selected_products = []
        self.time_spent = 0

        self.products_list = [
            ("Latte", 10), ("Mela", 2), ("Carne", 20), ("Pasta", 5),
            ("Cereali", 7), ("Uova", 3), ("Formaggio", 15), ("Pane", 4)
        ]

        self.start_time = time.time()

        self.timer_thread = QThread(self)
        self.timer_worker = TimerWorker(self.start_time)
        self.timer_worker.moveToThread(self.timer_thread)
        self.timer_worker.time_updated.connect(self.update_timer)
        self.timer_thread.started.connect(self.timer_worker.run)
        self.timer_thread.start()

    def accept_cart(self):
        self.time_spent = int(time.time() - self.start_time)
        self.selected_products = []

        spin_boxes = [
            self.spinBox, self.spinBox_2, self.spinBox_3, self.spinBox_4,
            self.spinBox_5, self.spinBox_6, self.spinBox_7, self.spinBox_8
        ]

        for i, spin_box in enumerate(spin_boxes):
            quantity = spin_box.value()
            if quantity > 0:
                product_name, price = self.products_list[i]
                for _ in range(quantity):
                    self.selected_products.append((i + 1000, product_name, price))

        self.cart_closed.emit(self.cliente_id, self.selected_products, self.time_spent)
        self.send_data_to_server()
        self.close()

    def reject_cart(self):
        self.selected_products = []
        self.time_spent = 0
        self.close()

    def update_timer(self, elapsed_time):
        self.label_9.setText(f"{elapsed_time} secondi")

    def closeEvent(self, event):
        self.timer_worker.stop()
        self.timer_thread.quit()
        self.timer_thread.wait()
        event.accept()

    def send_data_to_server(self):
        try:
            nProducts = len(self.selected_products)
            customer_data = struct.pack("iii", self.cliente_id, self.time_spent, nProducts)
            for product_id, name, price in self.selected_products:
                name_bytes = name.encode('utf-8').ljust(50, b'\0')
                customer_data += struct.pack("i50si", product_id, name_bytes, price)

            self.sock.sendall(customer_data)
            print(f"Cliente {self.cliente_id} inviato con {nProducts} prodotti e tempo di permanenza {self.time_spent} secondi.")
            self.sock.close()
        except Exception as e:
            print(f"Errore con il client {self.cliente_id}: {e}")


class TimerWorker(QObject):
    time_updated = pyqtSignal(int)

    def __init__(self, start_time):
        super().__init__()
        self.start_time = start_time
        self.running = True

    def run(self):
        while self.running:
            elapsed_time = int(time.time() - self.start_time)
            self.time_updated.emit(elapsed_time)
            time.sleep(1)

    def stop(self):
        self.running = False


class ClientDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.reject)

        self.cart_windows = []
        self.waiting_windows = []
        self.listaSpesaClienti = {}
        self.time_spent = {}

    def on_accept(self):
        num_clienti = self.spinBox.value()
        print(f"Apertura di {num_clienti} carrelli...")

        for cliente_id in range(num_clienti):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("127.0.0.1", 50000))

            client_id_data = struct.pack("i", cliente_id)
            sock.sendall(client_id_data)

            response = sock.recv(4).decode('utf-8')
            if response == "OK":
                cart_window = CartWindow(cliente_id, sock)
                self.cart_windows.append(cart_window)
                cart_window.cart_closed.connect(self.collect_cart_data)
                cart_window.show()
            elif response == "WAIT":
                waiting_window = WaitingWindow(cliente_id, sock)
                self.waiting_windows.append(waiting_window)
                waiting_window.show()

    def collect_cart_data(self, cliente_id, selected_products, time_spent):
        self.listaSpesaClienti[cliente_id] = selected_products
        self.time_spent[cliente_id] = time_spent
        print(f"Cliente {cliente_id} ha speso {time_spent} secondi.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ClientDialog()
    dialog.show()
    sys.exit(app.exec_())