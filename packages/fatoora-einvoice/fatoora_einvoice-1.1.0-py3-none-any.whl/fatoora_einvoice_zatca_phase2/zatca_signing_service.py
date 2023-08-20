
import os
import jpype.imports

if not jpype.isJVMStarted():
    jpype.startJVM(jpype.getDefaultJVMPath(), '-Djava.class.path='+os.getcwd()+'/java/zatca_update.jar')


from com.zatca import integrate

class SingDocument:
    def __init__(self):

        """
        Initializes the SingedClass class.
        """
        self.invoice_xml_base64 = None
        self.private_key = None
        self.certificate = None

    def sign_xml_document(self,invoice_xml_base64,private_key,certificate):
        var = integrate().process_sing_document(invoice_xml_base64, private_key, certificate)
        return str(var)

