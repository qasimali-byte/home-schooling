"""Modules"""
from collections import defaultdict
from datetime import datetime,date
import json
import hashlib
import hmac
import datetime as dt
import os
import urllib.parse
from functools import wraps
from math import sqrt
import requests
from flask import render_template
from flask_jwt_extended import create_access_token, get_jwt, verify_jwt_in_request
from jwt import ExpiredSignatureError
from flask_restful import abort
from flask_mail import Message
from fpdf import FPDF
import boto3
from botocore.exceptions import ClientError
from sentry_sdk import capture_exception
from config import (
    jwt,
    blacklist,
    mail,
    REACT_ROUTE,
    PROJECT_NAME,
    PROJECT_LOGO,
    AWS_ACCESS_KEY,
    AWS_SECRET_KEY,
    AWS_END_POINT,
    BUCKET_NAME,
)
from api import app


# This function is for setting role
def role(refresh, user_role):
    """Role Decorator"""

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request(refresh=refresh)
            except ExpiredSignatureError:
                abort(http_status_code=403, message="Token has expired")
            claims = get_jwt()
            if claims["role"] == user_role:
                return fn(*args, **kwargs)
            return abort(http_status_code=403, message=user_role + " only Tokens!")

        return decorator

    return wrapper


def jwt_required(refresh):
    """JWT Decorator"""

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request(refresh=refresh)
                return fn(*args, **kwargs)
            except ExpiredSignatureError:
                return abort(http_status_code=403, message="Token has expired")

        return decorator

    return wrapper


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    """Blacklisting JWT Token"""
    jti = jwt_payload["jti"]
    return jti in blacklist


# email_verification
def send_email_verification(email, name, user_id):
    """Sending Verification Email"""
    expires = dt.timedelta(days=30)
    token = create_access_token(identity=str(user_id), expires_delta=expires)
    msg = Message(
        subject="Email Verification",
        sender=app.config["MAIL_USERNAME"],
        recipients=[email],
    )
    msg.html = render_template(
        "email-verification.html",
        link=REACT_ROUTE + "/email-verification?token=" + token + "&email=" + email,
        email=email,
        user_name=name,
        website_name=PROJECT_NAME,
        react_route=REACT_ROUTE,
        logo=PROJECT_LOGO,
    )
    msg.body = f"""To Verfiy Your Account, visit following link:
    {REACT_ROUTE+'email-verification?token='+token+'&email='+email} {'Your Email is: '+email}"""
    mail.send(msg)

def send_subscription_fail_email(email, name):
    """Sending Subscription Fail Email"""
   
    msg = Message(
        subject="Payment Failure Notification - Action Required",
        sender=app.config["MAIL_USERNAME"],
        recipients=[email],
    )
    msg.html = render_template(
        "subscription_fail_email.html",
        email=email,
        user_name=name,
        website_name=PROJECT_NAME,
        react_route=REACT_ROUTE,
        logo=PROJECT_LOGO,
    )
    mail.send(msg)

def send_subscription_renewal_email(args, plan_data):
    """Sending Subscription renewal Email"""
   
    msg = Message(
        subject="Subscription Renewal Notification",
        sender=app.config["MAIL_USERNAME"],
        recipients=[args["email"]],
    )
    msg.html = render_template(
        "subscription_renew.html",
        email=args["email"],
        plan_name=plan_data["plan_name"],
        plan_duration=plan_data["plan_duration"],
        price=args["price"],
        website_name=PROJECT_NAME,
        react_route=REACT_ROUTE,
        logo=PROJECT_LOGO,
    )
    mail.send(msg)


# welcome_email
def send_welcome_email(email, name):
    """Sending welcome Email"""
    msg = Message(
        subject="Welcome", sender=app.config["MAIL_USERNAME"], recipients=[email]
    )
    msg.html = render_template(
        "welcome_email.html",
        email=email,
        user_name=name,
        website_name=PROJECT_NAME,
        react_route=REACT_ROUTE,
        logo=PROJECT_LOGO,
    )
    mail.send(msg)


# user_plans
def send_plan_email(email, p_name, p_duration, p_price):
    """Sending plan Email"""
    msg = Message(
        subject="Subscription Invoice",
        sender=app.config["MAIL_USERNAME"],
        recipients=[email],
    )
    msg.html = render_template(
        "user_plans.html",
        email=email,
        p_name=p_name,
        p_duration=p_duration,
        p_price=p_price,
        website_name=PROJECT_NAME,
        react_route=REACT_ROUTE,
        logo=PROJECT_LOGO,
    )
    mail.send(msg)





# helper functions for S3 functionality
def sign(key, msg):
    """for getting sign"""
    return hmac.new(key, msg.encode("utf8"), hashlib.sha256).digest()


def get_signature_key(key, date_stamp, region_name, service_name):
    "getting signature key"
    k_date = sign(("AWS4" + key).encode("utf8"), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, "aws4_request")
    return k_signing


def generate_aws_signature_v4_post_urls(object_keys):
    """Function to get upload urls"""
    method = "PUT"
    service = "s3"
    host = BUCKET_NAME + ".s3." + AWS_END_POINT + ".amazonaws.com"
    endpoint = "https://" + host

    # Get common signature elements once for efficiency
    amz_date = dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    datestamp = amz_date[:8]
    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = (
        datestamp + "/" + AWS_END_POINT + "/" + service + "/" + "aws4_request"
    )
    canonical_headers = "host:" + host + "\n"
    signed_headers = "host"

    # Generate URLs for each object key
    urls = []
    for object_key in object_keys:
        canonical_uri = "/" + object_key
        canonical_querystring = f"?X-Amz-Algorithm={algorithm}"
        canonical_querystring += f'&X-Amz-Credential={urllib.parse.quote_plus(AWS_ACCESS_KEY + "/" + credential_scope)}'
        canonical_querystring += f"&X-Amz-Date={amz_date}"
        canonical_querystring += f"&X-Amz-Expires=3600"
        canonical_querystring += f"&X-Amz-SignedHeaders={signed_headers}"
        canonical_request = f"{method}\n{canonical_uri}\n{canonical_querystring[1:]}\n{canonical_headers}\n{signed_headers}\nUNSIGNED-PAYLOAD"
        string_to_sign = f'{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()}'
        signing_key = get_signature_key(
            AWS_SECRET_KEY, datestamp, AWS_END_POINT, service
        )
        signature = hmac.new(
            signing_key, string_to_sign.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        canonical_querystring += f"&X-Amz-Signature={signature}"
        url = endpoint + canonical_uri + canonical_querystring
        urls.append(url)

    return urls


def generate_aws_signature_v4_get_urls(object_keys):
    """Function to get GET urls"""
    METHOD = "GET"
    SERVICE = "s3"
    host = BUCKET_NAME + ".s3." + AWS_END_POINT + ".amazonaws.com"
    endpoint = "https://" + host

    # Get common signature elements once for efficiency
    amz_date = dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    datestamp = amz_date[:8]
    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = (
        datestamp + "/" + AWS_END_POINT + "/" + SERVICE + "/" + "aws4_request"
    )
    canonical_headers = "host:" + host + "\n"
    signed_headers = "host"

    # Generate URLs for each object key
    urls = []
    for object_key in object_keys:
        canonical_uri = "/" + object_key
        canonical_querystring = f"?X-Amz-Algorithm={algorithm}"
        canonical_querystring += f'&X-Amz-Credential={urllib.parse.quote_plus(AWS_ACCESS_KEY + "/" + credential_scope)}'
        canonical_querystring += f"&X-Amz-Date={amz_date}"
        canonical_querystring += f"&X-Amz-Expires=3600"
        canonical_querystring += f"&X-Amz-SignedHeaders={signed_headers}"
        canonical_request = f"{METHOD}\n{canonical_uri}\n{canonical_querystring[1:]}\n{canonical_headers}\n{signed_headers}\nUNSIGNED-PAYLOAD"
        string_to_sign = f'{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()}'
        signing_key = get_signature_key(
            AWS_SECRET_KEY, datestamp, AWS_END_POINT, SERVICE
        )
        signature = hmac.new(
            signing_key, string_to_sign.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        canonical_querystring += f"&X-Amz-Signature={signature}"
        url = endpoint + canonical_uri + canonical_querystring
        urls.append(url)

    return urls


def list_s3_bucket_contents():
    """print all files in bucket"""
    s3 = boto3.client(
        "s3",
        region_name=AWS_END_POINT,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )

    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    for content in response.get("Contents", []):
        print(content["Key"])


def upload_file_to_s3(file_key):
    """upload a file to S3"""
    s3 = boto3.client(
        "s3",
        region_name=AWS_END_POINT,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )

    try:
        with open(file_key, "rb") as data:
            response = s3.upload_fileobj(data, BUCKET_NAME, file_key)
        return response

    except Exception as e:
        capture_exception(e)
        raise


def generate_download_url(object_key):
    s3_client = boto3.client(
        "s3",
        region_name=AWS_END_POINT,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )

    try:
        # Generate a pre-signed URL for the S3 object
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": object_key},
            ExpiresIn=3600,
        )

        return url

    except ClientError as e:
        raise


def delete_file_from_s3(file_key):
    """delete report.pdf before entering new"""
    s3 = boto3.client(
        "s3",
        region_name=AWS_END_POINT,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )
    try:
        response = s3.delete_object(Bucket=BUCKET_NAME, Key=file_key)
        return response

    except Exception as e:
        capture_exception(e)
        raise





# this code is for pdf generation
class PDF(FPDF):
    """PDF generating class"""

    def __init__(self):
        super().__init__()
        self.add_font("Arial", "", "arial.ttf", uni=True)

        self.line_spacing_factor = 0.5
        self.set_auto_page_break(auto=True, margin=10)

        # for header
        self.user_email = ""
        self.user_address = ""
        self.child_name = ""
        self.state_name = ""
        self.child_year = ""

        # for heading functions
        self.subject_heading = ""

        # for subject sub_heading function
        self.strand_subheading = ""
        self.substrand_subheading = ""
        self.code_subheading = ""
        self.code_desc_subheading = ""

        # for code heading and description
        self.substrand_code_subheading = ""

        # for activities
        self.act_start_date = ""
        self.act_end_date = ""
        self.act_desc = ""
        self.term_name = ""
        self.files = []
        self.file_links = []
        self.links = []

        # variables for json data
        self.elaboration = ""
        self.capabilities = ""


    def header_f(self):
        """PDF header function on first page"""

        self.image(
            "https://homeschoolingoz.com/wp-content/uploads/2019/12/hd-transparent-1-1536x1423.png",
            x=12,
            y=12,
            w=25,
        )

        self.set_text_color(34, 45, 92)
        self.set_font("Arial", "B", 24)
        self.set_xy(10, 15)
        self.cell(0, 10, "REPORT", 0, 1, "C")

        self.set_text_color(0, 0, 0)
        self.set_top_margin(10)
        self.set_font("Arial", "", 10)
        self.set_xy(135, 28)
        self.multi_cell(65, 10*self.line_spacing_factor, f"Email : {self.user_email}", 0, "L", 0)
        self.set_xy(135, 38)
        self.multi_cell(65, 10*self.line_spacing_factor, f"Address : {self.user_address}", 0, "L", 0)
        self.set_xy(135, 50)
        self.cell(0, 10, "Website : https://homeschoolingoz.com/", 0, 1, "L")
        
        self.set_top_margin(10)
        self.set_xy(10, 40)
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, f"{self.child_name}", 0, 1, "L")
        self.set_font("Arial", "", 12)
        self.cell(0, 10, f"{self.state_name}, {self.child_year}", 0, 1, "L")
        self.ln(1)
        
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    # def footer(self):
    #     """PDF footer function on every page"""
    #     self.set_y(-15)
    #     self.set_fill_color(243, 244, 246)
    #     self.rect(10, self.get_y(), 190, 10, "F")

    #     self.set_font("Arial", "I", 8)
    #     self.set_text_color(0, 0, 0)
    #     self.cell(0, 10, "https://homeschoolingoz.com/", 0, 0, "C")


    def rounded_rect(self, x, y, w, h, r, style="", corners="1234"):
        """function for rounded rectangle"""
        k = self.k
        hp = self.h
        if style == "F":
            op = "f"
        elif style == "FD" or style == "DF":
            op = "B"
        else:
            op = "S"
        myarc = 4 / 3 * (sqrt(2) - 1)
        self._out("%.2F %.2F m" % ((x + r) * k, (hp - y) * k))

        xc = x + w - r
        yc = y + r
        self._out("%.2F %.2F l" % (xc * k, (hp - y) * k))
        if "2" not in corners:
            self._out("%.2F %.2F l" % ((x + w) * k, (hp - y) * k))
        else:
            self._arc(xc + r * myarc, yc - r, xc + r, yc - r * myarc, xc + r, yc)

        xc = x + w - r
        yc = y + h - r
        self._out("%.2F %.2F l" % ((x + w) * k, (hp - yc) * k))
        if "3" not in corners:
            self._out("%.2F %.2F l" % ((x + w) * k, (hp - (y + h)) * k))
        else:
            self._arc(xc + r, yc + r * myarc, xc + r * myarc, yc + r, xc, yc + r)

        xc = x + r
        yc = y + h - r
        self._out("%.2F %.2F l" % (xc * k, (hp - (y + h)) * k))
        if "4" not in corners:
            self._out("%.2F %.2F l" % (x * k, (hp - (y + h)) * k))
        else:
            self._arc(xc - r * myarc, yc + r, xc - r, yc + r * myarc, xc - r, yc)

        xc = x + r
        yc = y + r
        self._out("%.2F %.2F l" % (x * k, (hp - yc) * k))
        if "1" not in corners:
            self._out("%.2F %.2F l" % (x * k, (hp - y) * k))
            self._out("%.2F %.2F l" % ((x + r) * k, (hp - y) * k))
        else:
            self._arc(xc - r, yc - r * myarc, xc - r * myarc, yc - r, xc, yc - r)
        self._out(op)

    def _arc(self, x1, y1, x2, y2, x3, y3):
        """function for rounded rectangle arc"""
        h = self.h
        self._out(
            "%.2F %.2F %.2F %.2F %.2F %.2F c "
            % (
                x1 * self.k,
                (h - y1) * self.k,
                x2 * self.k,
                (h - y2) * self.k,
                x3 * self.k,
                (h - y3) * self.k,
            )
        )


    def write_subject_heading(self):
        """PDF subject heading function"""

        self.ln(3)
        self.set_font("Arial", "B", 14)
        self.set_text_color(255, 255, 255)

        text = self.subject_heading
        box_width = 175
        box_start = 15
        self.set_fill_color(34, 45, 92)
        self.rounded_rect(box_start, self.get_y(), box_width, 10, 5, "F", "1234")
        self.cell(0, 10, text, 0, 1, "C", 0)

        self.ln(5)
        self.set_text_color(0, 0, 0)


    def write_subheading(self):
        """PDF subheading function"""
        self.set_font("Arial", "B", 12)
        self.set_fill_color(255,255,255)
        self.set_text_color(75, 85, 109)
        subheading_text = f"{self.code_subheading}  |  {self.strand_subheading}  |  {self.substrand_subheading}"        
        self.multi_cell(0, 10*self.line_spacing_factor, subheading_text, 0, "L", 1)
        self.ln(3)

        self.set_fill_color(255,255,255)
        self.set_text_color(0, 0, 0)
    
        self.set_font("Arial", "B", 10)
        self.set_x(15)
        self.cell(0, 10, "Code Description", 0, 1, "L")

        self.set_font("Arial", "", 10)
        self.set_x(self.get_x() + 10)
        self.multi_cell(0, 10*self.line_spacing_factor, f"{self.code_desc_subheading}", 0, "L", 1)
        self.ln(5)


    def write_subject_code_details(self):
        """PDF date details function"""   

        # ===== Code for Activity date & term =====
        self.set_text_color(255, 255, 255)
        self.set_x(15)
        self.set_font("Arial", "B", 10)
        self.ln(3)

        act_date_string = "Activity Start Date : " + self.act_start_date
        if self.act_end_date:
            act_date_string += f"  -  Activity End Date : {self.act_end_date}"

        box_width = 135
        box_start = 40
        self.set_fill_color(34, 45, 92)
        self.rounded_rect(box_start, self.get_y(), box_width, 10, 5, "F", "1234")
        self.cell(0, 10, act_date_string, 0, 1, "C", 0)

        # self.multi_cell(0, 10, act_date_string, 0, "C", 1)

        if self.term_name:
            self.set_x(100)
            self.set_y(self.get_y() - 10)
            term_string = "Term "+ str(self.term_name)
            self.cell(0, 10, term_string, 0, 1, "R")

        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)
        self.ln(3)


        # ===== Code for Activity description =====
        self.set_x(15)
        self.set_font("Arial", "B", 10)
        self.cell(0, 10, "User Description", 0, 1, "L")

        self.set_x(self.get_x() + 10)
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 10*self.line_spacing_factor, f"{self.act_desc}", 0, "L", 1)
        self.ln(3)


        # ===== Code for Activity elaboration =====
        if self.elaboration:
            self.set_x(15)
            self.set_font("Arial", "B", 10)
            self.cell(0, 10, "Elaboration", 0, 1, "L")

            self.set_x(self.get_x() + 10)
            self.set_font("Arial", "", 10)
            self.multi_cell(0, 10*self.line_spacing_factor, f"{self.elaboration}", 0, "L", 1)
            self.ln(3)


        # ===== Code for Activity GC =====
        if self.capabilities:
            self.set_x(15)
            self.set_font("Arial", "B", 10)
            self.cell(0, 10, "General Capabilities", 0, 1, "L")

            self.set_x(self.get_x() + 10)
            self.set_font("Arial", "", 10)
            self.multi_cell(0, 10*self.line_spacing_factor, f"{self.capabilities}", 0, "L", 1)
            self.ln(3)


        # ===== Code for Activity links =====
        if self.links:
            self.set_x(15)
            self.set_font("Arial", "B", 10)
            self.cell(0, 10, "Links", 0, 1, "L")
            for link in self.links:
                self.set_x(self.get_x() + 10)
                self.set_font("Arial", "", 10)
                self.set_text_color(34, 45, 92)
                self.multi_cell(0, 10*self.line_spacing_factor, f"{link}", 0, "L", 1)


        # ===== Code for Activity files =====
        VALID_IMAGE_EXTENSIONS = [
            ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".PNG", ".JPG", ".JPEG", ".GIF", ".BMP",
            ".ico", ".svg", ".webp", ".tiff", ".tif", ".ICO", ".SVG", ".WEBP", ".TIFF", ".TIF"
        ]

        if self.files:
            self.set_x(15)
            self.set_text_color(0, 0, 0)
            self.set_font("Arial", "B", 10)
            self.cell(0, 10, "Files", 0, 1, "L")

            for i, (file_name, file_link) in enumerate(zip(self.files, self.file_links)):
                self.set_x(self.get_x() + 10)
                self.set_font("Arial", "", 10)
                self.set_text_color(34, 45, 92)
                self.cell(0, 10*self.line_spacing_factor, f"{file_name}", 0, 1, "L", link=file_link)

                file_ext = os.path.splitext(file_name)[1].upper()
                if file_ext in VALID_IMAGE_EXTENSIONS:
                    download_link = generate_download_url(file_name)
                    response = requests.get(download_link)

                    if response.status_code == 200:
                        local_file_path = f"pdf_image_{i}{file_ext}"
                        with open(local_file_path, "wb") as f:
                            f.write(response.content)

                        if os.path.getsize(local_file_path) > 0:
                            with open(local_file_path, "rb") as f:
                                header = f.read(8)

                                image_type = ''
                                if header[:3] == b"\xFF\xD8\xFF":
                                    image_type = 'JPEG'
                                elif header[:4] == b"\x89\x50\x4E\x47":
                                    image_type = 'PNG'
                                elif header[:6] == b"\x47\x49\x46\x38\x37\x3A":
                                    image_type = 'GIF'
                                elif header[:2] == b"\x42\x4D":
                                    image_type = 'BMP'
                                else:
                                    pass

                                if image_type:
                                    available_width = self.w - self.get_x()  # Access width directly
                                    available_height = self.h - self.get_y() - self.b_margin  # Access height directly

                                    if image_type in ['JPEG', 'PNG']:
                                        image_width, image_height = 15 , 15
                                        if image_width > available_width or image_height > available_height:
                                            scale_factor = min(available_width / image_width, available_height / image_height)
                                            image_width = int(image_width * scale_factor)
                                            image_height = int(image_height * scale_factor)

                                    self.image(local_file_path, self.get_x() + 15, self.get_y() + 2, image_width, image_height, image_type)


                        os.remove(local_file_path)

                    self.ln(20)
        
        # self.ln(5)
        # self.set_x(15)
        # self.set_font("Arial", "B", 10)
        # self.set_text_color(0, 0, 0) 
        # dotted_line = "< " + "= "*10 + ">"
        # self.multi_cell(0, 10,dotted_line, 0, "C", 1)

        # self.set_line_width(0.5)
        # self.line(80, self.get_y(), 125, self.get_y())
        self.ln(5)



# helper functions for report pdf export
def process_pdf_header(pdf, first_activity):
    pdf.child_name = first_activity.get("child_name", "")
    pdf.state_name = first_activity.get("state_name", "")
    pdf.child_year = first_activity.get("school_year", "")
    pdf.user_email = first_activity.get("email", "")
    pdf.user_address = first_activity.get("address", "")
    pdf.header_f()

def process_pdf_content(pdf, activities_list , check):
    for act_obj in activities_list:
        pdf.act_start_date = act_obj.get("act_start_date", "")
        pdf.act_end_date = act_obj.get("act_end_date", "")
        pdf.act_desc = act_obj.get("activity_description", "")
        if check:
            pdf.term_name = act_obj.get("state_terms_id", "")

        pdf.links = act_obj.get("attached_links", "").split(",") if act_obj.get("attached_links") else []
        pdf.files = act_obj.get("attached_files_names", [])
        pdf.file_links = act_obj.get("attached_files_urls", [])

        if "json_subject_data" in act_obj:
            json_subject_data = act_obj.get("json_subject_data")
            
            pdf.elaboration = json_subject_data.get("Elaboration", "")

            gcc = json_subject_data.get("GCC", "")
            gcc_element = json_subject_data.get("Element", "")
            gcc_subelement = json_subject_data.get("SubElement", "")
            
            if gcc:
                pdf.capabilities = f"General capabilities are {gcc}"
                if gcc_element:
                    pdf.capabilities += f", {gcc_element}"
                if gcc_subelement:
                    pdf.capabilities += f", {gcc_subelement}"
            else:
                pdf.capabilities = ""

        
        pdf.write_subject_code_details()



# helper functions for view activities and making proper json to return
def process_file_array(file_array_str):
    """ Process file_array and return files_ids, files_names, and S3_files_urls. """

    try:
        file_array = json.loads(file_array_str) if file_array_str else []

        if not file_array or any(not file_entry.get("id") or not file_entry.get("file_name") for file_entry in file_array):
            return None, None, None
        
        attached_files_ids, attached_files_names = zip(*((file_entry["id"], file_entry["file_name"]) for file_entry in file_array))
        attached_files_urls = generate_aws_signature_v4_get_urls(attached_files_names)
        return attached_files_ids, attached_files_names, attached_files_urls

    except (json.JSONDecodeError, TypeError) as e:
        return None, None, None

def process_activities_for_subjects_view(activities):

    for activity in activities:
        start_date = activity.get("act_start_date")
        end_date = activity.get("act_end_date")
        created_date = activity.get("created_date")
        last_updated_date = activity.get("last_updated_date")
        file_array_str = activity["file_array"]
        attached_files_ids, attached_files_names, attached_files_urls = process_file_array(file_array_str)
        activity["attached_files_ids"] = attached_files_ids
        activity["attached_files_names"] = attached_files_names
        activity["attached_files_urls"] = attached_files_urls

        formatted_start_date = (
            start_date if isinstance(start_date, date) else
            datetime.strptime(start_date, "%a, %d %b %Y %H:%M:%S %Z").date()
        ).strftime("%d-%m-%Y")

        formatted_end_date = None
        if end_date:
            formatted_end_date = (
                end_date if isinstance(end_date, date) else
                datetime.strptime(end_date, "%a, %d %b %Y %H:%M:%S %Z").date()
            ).strftime("%d-%m-%Y")
        
        formatted_created_date = None
        if created_date:
            formatted_created_date = (
                created_date if isinstance(created_date, date) else
                datetime.strptime(created_date, "%a, %d %b %Y %H:%M:%S %Z").date()
            ).strftime("%d-%m-%Y")
        
        formatted_last_updated_date = (
            last_updated_date if isinstance(last_updated_date, date) else
            datetime.strptime(last_updated_date, "%a, %d %b %Y %H:%M:%S %Z").date()
        ).strftime("%d-%m-%Y")

        activity["act_start_date"] = formatted_start_date
        activity["act_end_date"] = formatted_end_date
        activity["created_date"] = formatted_created_date
        activity["last_updated_date"] = formatted_last_updated_date

    return activities



# helper functions for formatting json subject data
def append_data(entry, parsed_data):
    elaborations = parsed_data.get("Elaboration", [])
    if elaborations is not None:
        if isinstance(elaborations, str):
            elaborations = [elaborations]
        entry["elaborations"].extend(elaborations)

    if parsed_data.get("GC"):
        gcc_item = parse_gcc(parsed_data)
        existing_gcc = next((item for item in entry["gcc"] if item["GC"] == gcc_item["GC"]), None)
        if existing_gcc:
            existing_gcc["elements"].extend(gcc_item["elements"])
        else:
            entry["gcc"].append(gcc_item)

    if parsed_data.get("CCP"):
        entry["ccp"].append(parsed_data["CCP"])

def parse_code(parsed_data):
    code = parsed_data.get("CdCode")
    formatted_item = {
        "code": code,
        "description": parsed_data.get("ContentDesc", ""),
        "elaborations": [],
        "gcc": [],
        "ccp": []
    }

    elaborations = parsed_data.get("Elaboration", [])
    if elaborations is not None:
        if isinstance(elaborations, str):
            elaborations = [elaborations]
        formatted_item["elaborations"].extend(elaborations)

    if parsed_data.get("GC"):
        gcc_item = parse_gcc(parsed_data)
        existing_gcc = next((item for item in formatted_item["gcc"] if item["GC"] == gcc_item["GC"]), None)
        if existing_gcc:
            existing_gcc["elements"].extend(gcc_item["elements"])
        else:
            formatted_item["gcc"].append(gcc_item)

    if parsed_data.get("CCP"):
        formatted_item["ccp"].append(parsed_data["CCP"])

    return formatted_item

def parse_gcc(parsed_data):
    gcc_item = {
        "GC": parsed_data["GC"],
        "elements": []
    }
    element = parsed_data.get("Element")
    if element:
        element_item = parse_element(parsed_data)
        gcc_item["elements"].append(element_item)
    return gcc_item

def parse_element(parsed_data):
    element = parsed_data.get("Element")
    element_item = {
        "Element": element,
        "sub_elements": []
    }
    subelement = parsed_data.get("Subelement")
    if subelement:
        subelement_item = parse_subelement(parsed_data)
        element_item["sub_elements"].append(subelement_item)
    return element_item

def parse_subelement(parsed_data):
    subelement = parsed_data.get("Subelement")
    subelement_item = {
        "Subelement": subelement
    }
    return subelement_item