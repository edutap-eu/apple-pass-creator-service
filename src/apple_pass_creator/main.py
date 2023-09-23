from io import BytesIO
import os
import pathlib
from fastapi import FastAPI, File, Response, UploadFile
from fastapi.responses import FileResponse, StreamingResponse


app = FastAPI()

# import passbook.models as pmodels
from edutap.wallet_apple import models as pmodels


# utils

rootdir = pathlib.Path(__file__).parent.parent.parent
static = rootdir / "static"


certs_dir = rootdir / "var" / "certs"
apple_root_certificate_file = certs_dir / "wwdr_certificate.pem"
key_file = certs_dir / "private.key"
certificate_file = certs_dir / "certificate.pem"                                                        



# /utils


def create_shell_pass(
    barcodeFormat=pmodels.BarcodeFormat.CODE128, serial="1234567890", name="John Doe"
):
    cardInfo = pmodels.StoreCard()
    cardInfo.addPrimaryField("name", name, "Name")
    stdBarcode = pmodels.Barcode(
        message="test barcode", format=barcodeFormat, altText="alternate text"
    )
    passfile = pmodels.Pass(
        storeCard=cardInfo,
        organizationName="Org Name",
        passTypeIdentifier="pass.demo.lmu.de",
        teamIdentifier="JG943677ZY",
        description="A Sample Pass",
        serialNumber=serial,
    )
    passfile.barcode = stdBarcode

    return passfile


@app.get("/")
async def root():
    return {"message": "Hello World"}


global_serial = 100000


@app.get("/demo-pass", response_class=FileResponse)
def demo_pass(password: str = "", serial: str = "1234567890", name: str = "John Doe"):
    global global_serial


    passfile = create_shell_pass(serial=str(global_serial), name=name)
    global_serial += 1
    passfile.addFile("icon.png", open(static / "white_square.png", "rb"))
    buf: BytesIO = passfile.create(certificate_file, key_file, apple_root_certificate_file, password)

    return Response(
        buf.getvalue(),
        media_type="application/vnd.apple.pkpass",
        headers={"Content-Disposition": 'attachment; filename="pass.pkpass"'},
    )
