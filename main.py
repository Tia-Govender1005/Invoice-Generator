import json
import os
from tkinter import *
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas


class InvoiceGenerator:

    def __init__(self, root):
        self.root = root
        self.root.title("Tia's Invoice Generator")
        self.root.geometry("600x750")

        self.file_name = ""  

        self.frame = Frame(self.root, bg="white")
        self.frame.place(x=0, y=0, width=600, height=750)

        Label(
            self.frame,
            text="Enter your company details",
            font=("times new roman", 24, "bold"),
            bg="lightblue",
            fg="green",
        ).place(x=50, y=10)

       
        Label(
            self.frame,
            text="Company Name",
            font=("times new roman", 14, "bold"),
            bg="white",
            fg="gray",
        ).place(x=50, y=70)
        self.company_name = Entry(
            self.frame, font=("times new roman", 14), bg="white"
        )
        self.company_name.place(x=250, y=70, width=280, height=30)

        Label(
            self.frame,
            text="Address",
            font=("times new roman", 14, "bold"),
            bg="white",
            fg="gray",
        ).place(x=50, y=120)
        self.address = Entry(
            self.frame, font=("times new roman", 14), bg="white"
        )
        self.address.place(x=250, y=120, width=280, height=30)

        Label(
            self.frame,
            text="City",
            font=("times new roman", 14, "bold"),
            bg="white",
            fg="gray",
        ).place(x=50, y=170)
        self.city = Entry(
            self.frame, font=("times new roman", 14), bg="white"
        )
        self.city.place(x=250, y=170, width=280, height=30)

        Label(
            self.frame,
            text="GST Number",
            font=("times new roman", 14, "bold"),
            bg="white",
            fg="gray",
        ).place(x=50, y=220)
        self.gst = Entry(
            self.frame, font=("times new roman", 14), bg="white"
        )
        self.gst.place(x=250, y=220, width=280, height=30)

        Label(
            self.frame,
            text="Date",
            font=("times new roman", 14, "bold"),
            bg="white",
            fg="gray",
        ).place(x=50, y=270)
        self.date = Entry(
            self.frame, font=("times new roman", 14), bg="white"
        )
        self.date.place(x=250, y=270, width=280, height=30)

        Label(
            self.frame,
            text="Contact",
            font=("times new roman", 14, "bold"),
            bg="white",
            fg="gray",
        ).place(x=50, y=320)
        self.contact = Entry(
            self.frame, font=("times new roman", 14), bg="white"
        )
        self.contact.place(x=250, y=320, width=280, height=30)

        Label(
            self.frame,
            text="Customer Name",
            font=("times new roman", 14, "bold"),
            bg="white",
            fg="gray",
        ).place(x=50, y=370)
        self.c_name = Entry(
            self.frame, font=("times new roman", 14), bg="white"
        )
        self.c_name.place(x=250, y=370, width=280, height=30)

        Label(
            self.frame,
            text="Authorized Signatory",
            font=("times new roman", 14, "bold"),
            bg="lightblue",
            fg="gray",
        ).place(x=50, y=420)
        self.aus = Entry(
            self.frame, font=("times new roman", 14), bg="white"
        )
        self.aus.place(x=250, y=420, width=280, height=30)

        Label(
            self.frame,
            text="Company Image",
            font=("times new roman", 14, "bold"),
            bg="lightblue",
            fg="gray",
        ).place(x=50, y=470)
        Button(
            self.frame,
            text="Browse Files",
            font=("times new roman", 12),
            command=self.browse,
        ).place(x=250, y=470)

        self.img_label = Label(
            self.frame,
            text="No image selected",
            font=("times new roman", 11, "italic"),
            bg="lightblue",
        )
        self.img_label.place(x=250, y=505)

    
        Button(
            self.frame,
            text="Submit Details",
            command=self.submit_invoice,
            font=("times new roman", 14, "bold"),
            fg="white",
            cursor="hand2",
            bg="#B00857",
        ).place(x=200, y=560, width=200, height=45)

    def browse(self):
        filename = filedialog.askopenfilename(title="Select Logo/Image")
        if filename:
            self.file_name = filename
            self.img_label.config(text=os.path.basename(self.file_name))

    def save_to_json(self, invoice_data):
        json_file = "invoices_data.json"
        existing_data = []

        if os.path.exists(json_file):
            try:
                with open(json_file, "r") as file:
                    existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []

        existing_data.append(invoice_data)

        with open(json_file, "w") as file:
            json.dump(existing_data, file, indent=4)

    def reset_fields(self):
        self.company_name.delete(0, END)
        self.address.delete(0, END)
        self.city.delete(0, END)
        self.gst.delete(0, END)
        self.date.delete(0, END)
        self.contact.delete(0, END)
        self.c_name.delete(0, END)
        self.aus.delete(0, END)
        self.file_name = ""
        self.img_label.config(text="No image selected")

    def submit_invoice(self):
        if not self.company_name.get() or not self.c_name.get():
            messagebox.showwarning(
                "Missing Data", "Please fill in at least Company and Customer Name!"
            )
            return

        invoice_record = {
            "company_name": self.company_name.get(),
            "address": self.address.get(),
            "city": self.city.get(),
            "gst": self.gst.get(),
            "date": self.date.get(),
            "contact": self.contact.get(),
            "customer_name": self.c_name.get(),
            "authorized_signatory": self.aus.get(),
            "logo_path": self.file_name,
        }

    
        self.save_to_json(invoice_record)

       
        download_pdf = messagebox.askyesno(
            "Success & Thank You!",
            "Thank you! Your invoice data has been saved successfully.\n\n"
            ,
        )

        # if download_pdf:
        #     self.generate_pdf()
        #     messagebox.showinfo(
        #         "PDF Generated", "Invoice PDF created successfully!"
        #     )

        self.reset_fields()

    def generate_pdf(self):
        output_filename = f"Invoice_{self.c_name.get().replace(' ', '_')}.pdf"
        c = canvas.Canvas(output_filename, pagesize=(200, 250), bottomup=0)
        c.setFillColorRGB(0.8, 0.5, 0.7)

        c.line(70, 22, 180, 22)
        c.line(5, 45, 195, 45)
        c.line(15, 120, 185, 120)
        c.line(35, 108, 35, 220)
        c.line(115, 108, 115, 220)
        c.line(135, 108, 135, 220)
        c.line(160, 108, 160, 220)
        c.line(15, 220, 185, 220)

        if self.file_name and os.path.exists(self.file_name):
            c.translate(10, 40)
            c.scale(1, -1)
            c.drawImage(self.file_name, 0, 0, width=50, height=30)
            c.scale(1, -1)
            c.translate(-10, -40)

        c.setFont("Times-Bold", 10)
        c.drawCentredString(125, 20, self.company_name.get())

        c.setFont("Times-Bold", 5)
        c.drawCentredString(125, 30, self.address.get())
        c.drawCentredString(125, 35, self.city.get())
        c.setFont("Times-Bold", 6)
        c.drawCentredString(125, 42, "GST No:" + self.gst.get())

        c.setFont("Times-Bold", 8)
        c.drawCentredString(100, 55, "INVOICE")

        c.setFont("Times-Bold", 5)
        c.drawRightString(70, 70, "Invoice No. :")
        c.drawRightString(100, 70, "XXXXXXX")

        c.drawRightString(70, 80, "Date :")
        c.drawRightString(100, 80, self.date.get())

        c.drawRightString(70, 90, "Customer Name :")
        c.drawRightString(100, 90, self.c_name.get())

        c.drawRightString(70, 100, "Phone No. :")
        c.drawRightString(100, 100, self.contact.get())

        c.roundRect(15, 108, 170, 130, 10, stroke=1, fill=0)

        c.drawCentredString(25, 118, "S.No.")
        c.drawCentredString(75, 118, "Orders")
        c.drawCentredString(125, 118, "Price")
        c.drawCentredString(148, 118, "Qty.")
        c.drawCentredString(173, 118, "Total")

        c.drawString(30, 230, "This is a system generated invoice.")

        c.drawRightString(180, 228, self.aus.get())
        c.drawRightString(180, 235, "Signature")

        c.showPage()
        c.save()


if __name__ == "__main__":
    root = Tk()
    app = InvoiceGenerator(root)
    root.mainloop()