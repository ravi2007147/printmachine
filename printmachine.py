#!/usr/bin/python3
import time, pprint, cups
from woocommerce import API
import json
import pydf
import datetime
import pdfkit
from pdf2image import convert_from_path
import imgkit
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("url")
CONSUMER_KEY = os.getenv("consumer_key")
CONSUMER_SECRET = os.getenv("consumer_secret")
   
# conn = cups.Connection()
# printers = conn.getPrinters ()
# pprint.pprint(printers)
# print()
   
# printer = conn.getDefault()
# print("Default1:", printer)
   
# if printer == None:
#     printer = list(printers.keys())[0]
#     print("Default2:", printer)
   
# myfile = "./sample.pdf"
# pid = conn.printFile(printer, myfile, "test", {})
# while conn.getJobs().get(pid, None) is not None:
#     time.sleep(1)
# #done


class PrintMachine:
	def __init__(self):
		try:

			self.wcapi = API(
				url = URL,
				consumer_key = CONSUMER_KEY,
				consumer_secret = CONSUMER_SECRET,
				version = "wc/v3",
				wp_api=True,
				query_string_auth=True
			)

			# strr = "<table width='100%'><tr><td width='150'><img style='width:150px;height:150px;' src='https://shop.corner.ws/wp-content/uploads/2020/10/Corner-Logo.png' /></td><td style='padding-left:50px;'><b style='font-size:50px;'>Order : 2379</b><br /><br /><span style='font-size:45px;'><b>Date : 03 Sep 2021</b></span></td></tr></table><table width='100%' style='margin-top:100px;'><tr><td style='padding-bottom:20px;'><b style='font-size:40px;'>EASY BURGER</b></td><td width='100' align='center'><b style='font-size:40px;'>10</b></td></tr><tr><td style='padding-bottom:20px;'><b style='font-size:40px;'>CAPASANTA</b></td><td width='100' align='center'><b style='font-size:40px;'>1</b></td></tr><tr><td style='padding-bottom:20px;'><b style='font-size:40px;'>GAMBERI FRITTI</b></td><td width='100' align='center'><b style='font-size:40px;'>1</b></td></tr><tr><td style='padding-bottom:20px;'><b style='font-size:40px;'>HAM</b></td><td width='100' align='center'><b style='font-size:40px;'>1</b></td></tr><tr><td style='padding-bottom:20px;'><b style='font-size:40px;'>PIOVRA</b></td><td width='100' align='center'><b style='font-size:40px;'>1</b></td></tr><tr><td style='padding-bottom:20px;'><b style='font-size:40px;'>SALMONE MARINATO</b></td><td width='100' align='center'><b style='font-size:40px;'>1</b></td></tr><tr><td style='padding-bottom:20px;'><b style='font-size:40px;'>SCAMPI CRUDI</b></td><td width='100' align='center'><b style='font-size:40px;'>1</b></td></tr><tr><td style='padding-bottom:20px;'><b style='font-size:40px;'>TONNO TARTARE</b></td><td width='100' align='center'><b style='font-size:40px;'>1</b></td></tr><tr><td style='padding-bottom:20px;'><b style='font-size:40px;'>ABATE NERO “Cuvée dell’Abate” Riserva 2008</b></td><td width='100' align='center'><b style='font-size:40px;'>1</b></td></tr></table><table width='100%' style='margin-top:20px;'><tr><td>&nbsp;</td></tr><tr><td colspan='2' align='left'><div style='float:right;text-align:left;'><b style='font-size:40px;'>Subtotal : 195.09</b></div></td></tr><tr><td colspan='2'><div style='float:right;'><b style='font-size:40px;'>Tax : 42.91</b></div></td></tr><tr><td colspan='2'><div style='float:right;'><b style='font-size:40px;'>Total : 195.0942.91</b></div></td></tr></table><table width='100%' style='margin-top:50px;'><tr><td style='font-size:50px;'><b>Delivery Date : 03 Sep 2021</b></td></tr><tr><td style='font-size:50px;'><b>Delivery Time : 21:00 - 21:30</b></td></tr></table><table width='100%' style='margin-top:50px;'><tr><td style='font-size:45px;'><b>Payment Via Pagamento alla consegna on 03 Sep 2021 06:01 PM</b></td></tr></table><table width='100%' style='margin-top:80px;padding-bottom:50px;'><tr><td valign='top'><b style='font-size:40px;'>Billing Details<br /><span style='font-size:40px;'>Simone Palazzin<br />Via Segaluzza<br />33170<br />Pordenone<br />babaz.it@gmail.com<br />+3903294732551</span></b></td></tr></table><table width='100%' style='padding-bottom:80px;'><tr><td valign='top'><b style='font-size:40px;m'>Shipping Details<br /><span style='font-size:40px;'>Simone Palazzin<br />Via Segaluzza<br />33170<br />Pordenone</span></b></td></tr></table>" 


			# imgkit.from_string(strr, '/home/printmachine/output.jpg')


			# return;

			

			#json data get code
			r = self.wcapi.get("orders?printed=no&per_page=10")
			jdata = r.json()

			pdfstring=""
			orderfinalid = ""

			order = ""
#			print(jdata)
#			return
			for odr in jdata:
				try:
					if not odr["printed"] or odr["printed"] == "no":
						order = odr
						break
				except:
					print("error")
					#order = odr
					err=""
			print(order)
			
			if order:
				orderfinalid = str(order["id"])

				# print(order["customer_note"])

				

				#update code
				# print(order)
				# print(orderfinalid)
				
				# print(order["date_created"])

				datetime_object=datetime.datetime.strptime(order["date_created"], "%Y-%m-%dT%H:%M:%S")
				# paytime_object=datetime.datetime.strptime(order["date_paid"], "%Y-%m-%dT%H:%M:%S")

				pmethod = ""

				if "paymentmethod" in order:
					pmethod = order["paymentmethod"]

				ptrans = ""

				if "transaction_id" in order:
					if order["transaction_id"]:
						ptrans = "<tr><td colspan='2'>Transaction ID : "+str(order["transaction_id"])+"</td></tr>"

				
				print(datetime_object.strftime("%d %b %Y"))
				pdfstring = pdfstring + "<table width='100%'><tr><td width='150'><img style='width:150px;height:150px;' src='https://shop.corner.ws/wp-content/uploads/2020/10/Corner-Logo.png' /></td><td style='padding-left:50px;'><b style='font-size:50px;'>Order : "+str(order["id"])+"</b><br /><br /><span style='font-size:45px;'><b>Date : "+str(datetime_object.strftime("%d %b %Y"))+"</b></span></td></tr></table>"
				
				# <table width='100%'><tr><td>Order : "+str(order["id"])+"</td></tr><tr><td>Date : "+str(datetime_object.strftime("%d %b %Y"))+"</td></tr><tr><td colspan='2'>Payment Via "+str(pmethod)+" on "+str(datetime_object.strftime("%d %b %Y %I:%M %p"))+"</td></tr>"+ptrans+"<tr><td colspan='2'><hr /></td></tr></table>

				pdfstring = pdfstring + "<table width='100%' style='margin-top:100px;'>"
				subtotal = 0.0
				taxtotal = 0.0
				for lineitem in order["line_items"]:
					
					subtotal = subtotal + float("{:.2f}".format(float(lineitem["subtotal"])))
					taxtotal = taxtotal + float("{:.2f}".format(float(lineitem["total_tax"])))

					# print(taxtotal)
					pdfstring = pdfstring + "<tr><td style='padding-bottom:20px;'><b style='font-size:40px;'>"+str(lineitem["name"])+"</b></td><td width='100' align='center'><b style='font-size:40px;'>"+str(lineitem["quantity"])+"</b></td></tr>"

				pdfstring = pdfstring + "</table>";

				# print((subtotal+taxtotal))
				pdfstring = pdfstring + "<table width='100%' style='margin-top:20px;'><tr><td>&nbsp;</td></tr><tr><td colspan='2' align='left'><div style='float:right;text-align:left;'><b style='font-size:40px;'>Subtotal : "+str("{:.2f}".format(subtotal))+"</b></div></td></tr><tr><td colspan='2'><div style='float:right;'><b style='font-size:40px;'>Tax : "+str("{:.2f}".format(taxtotal))+"</b></div></td></tr><tr><td colspan='2'><div style='float:right;'><b style='font-size:40px;'>Total : "+(str(subtotal+taxtotal))+"</b></div></td></tr></table>"

				



				billinginfo = order["billdetails"][0]

				if (len(order["billdetails"])>1):
					shippinginfo = order["billdetails"][1]
				else:
					shippinginfo = ""

				if (len(order["billdetails"])>2):
					deliveryinfo = order["billdetails"][2]
				else:
					deliveryinfo = ""

				# print(billinginfo)

				deliverystring = ""
				swidth = "33.3%" 

				if deliveryinfo:

					dltype = deliveryinfo.get("deliverytype")



					if dltype == "non-deliverable":
						# deliverystring = deliverystring + "</tr><tr><td colspan='3'><hr /></td></tr>"
						swidth = "50%"
					else:
						
						if deliveryinfo.get("deliverytype") == "pickup":
							dltype = "Pickup"

						if deliveryinfo.get("deliverytype") == "delivery":
							dltype = "Home Delivery"

						if deliveryinfo.get("deliverytype") == "non-deliverable":
							dltype = "Non Deliverable"

						# if deliveryinfo.get("deliverytype") == "delivery":
						# deliverystring = deliverystring + "<td width='"+swidth+"' valign='top'><table width='100%'><tr><td><b>Delivery Details</b></td></tr><tr><td>Delivery Type : "+dltype+"</td></tr>"

						if deliveryinfo.get("deliverytype") == "delivery":
							dldetail = ""
							# pdfstring = pdfstring + "<table width='100%' style='margin-top:50px;'>"

							if "deliverydate" in deliveryinfo:
								if deliveryinfo.get("deliverydate"):
									dldatetime_object=datetime.datetime.strptime(deliveryinfo.get("deliverydate"), "%Y/%m/%d")
									dldetail = dldetail + "<tr><td style='font-size:50px;'><b>Delivery Date : "+str(dldatetime_object.strftime("%d %b %Y"))+"</b></td></tr>"

							if "pi_delivery_time" in deliveryinfo:
								if deliveryinfo.get("pi_delivery_time"):
									dldetail = dldetail + "<tr><td style='font-size:50px;'><b>Delivery Time : "+deliveryinfo.get("pi_delivery_time")+"</b></td></tr>"


							
							if dldetail:
								pdfstring = pdfstring + "<table width='100%' style='margin-top:50px;'>"+dldetail+"</table>"



						if deliveryinfo.get("deliverytype") == "pickup":
							dldetail = ""
							# pdfstring = pdfstring + "<table width='100%' style='margin-top:50px;'>"

							if "deliverydate" in deliveryinfo:
								if deliveryinfo.get("deliverydate"):
									dldatetime_object=datetime.datetime.strptime(deliveryinfo.get("deliverydate"), "%Y/%m/%d")
									dldetail = dldetail + "<tr><td style='font-size:50px;'><b>Pickup Date : "+str(dldatetime_object.strftime("%d %b %Y"))+"</b></td></tr>"

							if "pi_delivery_time" in deliveryinfo:
								if deliveryinfo.get("pi_delivery_time"):
									dldetail = dldetail + "<tr><td style='font-size:50px;'><b>Pickup Time : "+deliveryinfo.get("pi_delivery_time")+"</b></td></tr>"

							if dldetail:
								pdfstring = pdfstring + "<table width='100%' style='margin-top:50px;'>"+dldetail+"</table>"

				pdfstring = pdfstring + "<table width='100%' style='margin-top:50px;'><tr><td style='font-size:45px;'><b>Notes<br />"+str(order["customer_note"])+"</b></td></tr></table>"

				pdfstring = pdfstring + "<table width='100%' style='margin-top:50px;'><tr><td style='font-size:45px;'><b>Payment Via "+str(pmethod)+" on "+str(datetime_object.strftime("%d %b %Y %I:%M %p"))+"</b></td></tr></table>"
						
				# pdfstring = pdfstring + ""

				if billinginfo:
					pdfstring = pdfstring + "<table width='100%' style='margin-top:80px;padding-bottom:50px;'><tr><td valign='top'><b style='font-size:40px;'>Billing Details<br /><span style='font-size:40px;'>"+str(billinginfo.get("name"))+"<br />"+str(billinginfo.get("address"))+"<br />"+str(billinginfo.get("postcode"))+"<br />"+str(billinginfo.get("city"))+"<br />"+str(billinginfo.get("email"))+"<br />"+str(billinginfo.get("phonenumber"))+"</span></b></td></tr></table>"
					
					
					

				if shippinginfo:
					pdfstring =pdfstring + "<table width='100%' style='padding-bottom:80px;'><tr><td valign='top'><b style='font-size:40px;m'>Shipping Details<br /><span style='font-size:40px;'>"+str(billinginfo.get("name"))+"<br />"+str(billinginfo.get("address"))+"<br />"+str(billinginfo.get("postcode"))+"<br />"+str(billinginfo.get("city"))+"</span></b></td></tr></table>"
					
					

				
				# pdfstring = pdfstring + deliverystring


				# pdfstring = pdfstring + "</table>"

				

			#pdfstring = pdfstring + ""

			

			# #generate pdf code

			print(pdfstring)

			if pdfstring:
				pdfkit.from_string(pdfstring,'test_doc.pdf')
			else:
				return;
				# pdf = pydf.generate_pdf(pdfstring)
				# with open('test_doc.pdf','wb') as f:
				# 	f.write(pdf)

			conn = cups.Connection()
			printers = conn.getPrinters ()
			# pprint.pprint(printers)
			# # print()
			   
			printer = conn.getDefault()
			# # print("Default1:", printer)
			   
			if printer == None:
			    printer = list(printers.keys())[0]
			#     # print("Default2:", printer)

			# lp -d woocomm1 test_doc.pdf
			# system("lp -d MyPrinter " + file)
			   
			myfile = "./test_doc.pdf"
			# images = convert_from_path(myfile)

			# for img in images:
			# 	img.save('output.jpg', 'JPEG')

			path = "/home/printmachine/output.jpg";

			imgkit.from_string(pdfstring, path)

			print(printer)
			print("printer name")

			pid = conn.printFile(printer, path, "test", {})
			print(pid)
			while conn.getJobs().get(pid, None) is not None:
			    time.sleep(1)
			# # #done

			data={
					"printed":"yes"
				}

			self.wcapi.put("orders/"+orderfinalid,data).json()
		except Exception as e:
			print("exception")
			print((e))

		

		

p = PrintMachine()
