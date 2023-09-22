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


def certs_dir() -> pathlib.PosixPath:
    return rootdir / "var" / "certs"


apple_root_certificate = certs_dir() / "wwdr_certificate.pem"


def get_cert_file(cert_name: str):
    return open(certs_dir() / cert_name + ".pem", "rb")


def get_cert_file_path(cert_name: str = "certificate"):
    return str(certs_dir() / cert_name) + ".pem"


def get_key_file_path(cert_name: str = "certificate"):
    return str(certs_dir() / cert_name) + ".key"


def get_cert(cert_name: str) -> bytes:
    with open(certs_dir() / cert_name, "rb") as f:
        return f.read()


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
        passTypeIdentifier="Pass Type ID",
        teamIdentifier="Team Identifier",
        description="A Sample Pass",
        serialNumber=serial,
    )
    passfile.barcode = stdBarcode
    # passfile.serialNumber = serial
    # passfile.description = "A Sample Pass"
    # passfile.teamIdentifier = "JG943677ZY"
    # passfile.passTypeIdentifier = "pass.demo.lmu.de"
    return passfile


def create_shell_pass_orig(
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
        passTypeIdentifier="Pass Type ID",
        teamIdentifier="Team Identifier",
        description="A Sample Pass",
        serialNumber=serial,
    )
    passfile.barcode = stdBarcode
    # passfile.serialNumber = serial
    # passfile.description = "A Sample Pass"
    # passfile.teamIdentifier = "JG943677ZY"
    # passfile.passTypeIdentifier = "pass.demo.lmu.de"
    return passfile


@app.get("/")
async def root():
    return {"message": "Hello World"}


global_serial = 100000


@app.get("/demo-pass", response_class=FileResponse)
def demo_pass(password: str = "", serial: str = "1234567890", name: str = "John Doe"):
    global global_serial
    certpath = get_cert_file_path()
    keypath = get_key_file_path()
    print(certpath)

    passfile = create_shell_pass(serial=str(global_serial), name=name)
    global_serial += 1
    passfile.addFile("icon.png", open(static / "white_square.png", "rb"))
    buf: BytesIO = passfile.create(certpath, keypath, apple_root_certificate, password)

    return Response(
        buf.getvalue(),
        media_type="application/vnd.apple.pkpass",
        headers={"Content-Disposition": 'attachment; filename="pass.pkpass"'},
    )

@app.get("/demo-pass-orig", response_class=FileResponse)
def demo_pass(password: str = "", serial: str = "1234567890", name: str = "John Doe"):
    global global_serial
    certpath = get_cert_file_path()
    keypath = get_key_file_path()
    print(certpath)

    passfile = create_shell_pass(serial=str(global_serial), name=name)
    global_serial += 1
    passfile.addFile("icon.png", open(static / "white_square.png", "rb"))
    buf: BytesIO = passfile.create(certpath, keypath, apple_root_certificate, password)

    return Response(
        buf.getvalue(),
        media_type="application/vnd.apple.pkpass",
        headers={"Content-Disposition": 'attachment; filename="pass.pkpass"'},
    )