import sys
import struct
import socket
from PyQt5.QtWidgets import QApplication, QDialog
from client_ui import Ui_Dialog  # UI principale
from cart import Ui_Dialog as Ui_CartDialog  # UI del carrello (rinominata)

class CartWindow(QDialog, Ui_CartDialog):  # Ora usa la UI corretta
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept_cart)
        self.buttonBox.rejected.connect(self.close)  # Usa close() invece di reject()

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

    def accept_cart(self):
        """Recupera i prodotti selezionati e chiude la finestra."""
        self.selected_products = []

        spin_boxes = [
            self.spinBox, self.spinBox_2, self.spinBox_3, self.spinBox_4,
            self.spinBox_5, self.spinBox_6, self.spinBox_7, self.spinBox_8, self.spinBox_9
        ]

        for i, spin_box in enumerate(spin_boxes):
            quantity = spin_box.value()
            if quantity > 0:
                product_name, price = self.products_list[i]
                for _ in range(quantity):
                    self.selected_products.append((i + 1000, product_name, price))

        self.accept()  # Chiude il dialogo con successo

class MyClientDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.reject)

    def on_accept(self):
        num_clienti = self.spinBox.value()  # Numero di clienti scelti
        print(f"Invio {num_clienti} clienti al server...")

        for cliente_id in range(1, num_clienti + 1):
            cart_window = CartWindow()
            if cart_window.exec_():
                products = cart_window.selected_products
                nProducts = len(products)

                if nProducts == 0:
                    print(f"Cliente {cliente_id} ha un carrello vuoto, non verrà inviato.")
                    continue  # Salta il cliente se non ha prodotti

                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect(("127.0.0.1", 50000))

                    time = 10  # Simuliamo un tempo di permanenza fisso
                    customer_data = struct.pack("iii", cliente_id, time, nProducts)

                    for product_id, name, price in products:
                        name_bytes = name.encode('utf-8').ljust(50, b'\0')
                        customer_data += struct.pack("i50si", product_id, name_bytes, price)

                    sock.sendall(customer_data)
                    print(f"Cliente {cliente_id} inviato con {nProducts} prodotti.")

                    sock.close()
                except Exception as e:
                    print(f"Errore con il client {cliente_id}: {e}")

        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = MyClientDialog()
    if dialog.exec_():
        print("Dialogo chiuso con OK")
    else:
        print("Dialogo chiuso con Cancel")
    sys.exit(app.exec_())
