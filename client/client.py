import sys
import struct
import socket
import threading
import time
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout

from client_ui import Ui_Dialog  # UI principale
from cart import Ui_Dialog as Ui_CartDialog  # UI del carrello (rinominata)

class CartWindow(QDialog, Ui_CartDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept_cart)
        self.buttonBox.rejected.connect(self.close)

        # Lista dei prodotti con prezzi fissi
        self.products_list = [
            ("Latte", 10),
            ("Mela", 2),
            ("Carne", 20),
            ("Pasta", 5),
            ("Cereali", 7),
            ("Uova", 3),
            ("Formaggio", 15),
            ("Pane", 4),
            ("Pasta", 5)
        ]

        # Inizializza il cronometro
        self.start_time = time.time()
        self.running = True
        self.timer_thread = threading.Thread(target=self.update_timer)
        self.timer_thread.start()

    def update_timer(self):
        while self.running:
            time.sleep(1)
            self.time_spent = int(time.time() - self.start_time)
            self.label_9.setText(f"{self.time_spent} secondi")

    def accept_cart(self):
        """Recupera i prodotti selezionati e chiude la finestra."""
        self.running = False
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

        self.accept()  # Chiude il dialogo con successo

class ClientDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.reject)
        self.time_spent = 0

    def on_accept(self):
        num_clienti = self.spinBox.value()  # Numero di clienti scelti
        print(f"Invio {num_clienti} clienti al server...")

        for cliente_id in range(1, num_clienti + 1):
            cart_window = CartWindow()
            if cart_window.exec_():
                products = cart_window.selected_products
                self.time_spent = cart_window.time_spent  # Update with actual time spent
                nProducts = len(products)

                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect(("127.0.0.1", 50000))

                    customer_data = struct.pack("iii", cliente_id, self.time_spent, nProducts)

                    for product_id, name, price in products:
                        name_bytes = name.encode('utf-8').ljust(50, b'\0')
                        customer_data += struct.pack("i50si", product_id, name_bytes, price)

                    sock.sendall(customer_data)
                    print(f"Cliente {cliente_id} inviato con {nProducts} prodotti e tempo di permanenza {self.time_spent} secondi.")

                    sock.close()
                except Exception as e:
                    print(f"Errore con il client {cliente_id}: {e}")

        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ClientDialog()
    if dialog.exec_():
        print("Dialogo chiuso con OK")
        exit(0)
    else:
        print("Dialogo chiuso con Cancel")
        exit(1)