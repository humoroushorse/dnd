"""Python script for populating seed data in a fresh database."""
import requests
from pydantic import BaseModel


class TempReport(BaseModel):
    """Database seed load report."""

    created: int
    errored: int
    warning: int


report = TempReport(created=0, errored=0, warning=0)


# TODO: pure function
def update_report(report: TempReport, response: requests.Response, filename="") -> None:
    """Mutates a report by incrementing fields."""
    response_json: dict = response.json()
    totals: dict = response_json.get("totals", {})
    created = totals.get("created", 0)
    errored = totals.get("errored", 0)
    warning = totals.get("warning", 0)
    report.created += created
    report.errored += errored
    report.warning += warning

    def format_int(number: int) -> str:
        return f"{number:04d}"

    summary = {
        "created": format_int(created),
        "errored": format_int(errored),
        "warning": format_int(warning),
    }
    print(f"\t{summary} -> {filename}")  # noqa: T001


data_root = "app/dnd/test_data/json/seeds"
api_root = "http://127.0.0.1:8000/api/v1"
headers = {
    "accept": "application/json",
    # requests won't add a boundary if this header is set when you pass files=
    # 'Content-Type': 'multipart/form-data',
}

################################################################################
# 1. Source
################################################################################
files = {
    "upload_file": (
        "source.json",
        open(f"{data_root}/source.json", "rb"),
        "application/json",
    )
}
sources_response = requests.post(
    url=f"{api_root}/sources/bulk", files=files, headers=headers
)
update_report(report, sources_response, files.get("upload_file")[0])

################################################################################
# 2. Class
################################################################################
files = {
    "upload_file": (
        "class.json",
        open(f"{data_root}/class.json", "rb"),
        "application/json",
    )
}
class_response = requests.post(
    url=f"{api_root}/classes/bulk", files=files, headers=headers
)
update_report(report, sources_response, files.get("upload_file")[0])

################################################################################
# 3. Spells
################################################################################
files = {
    "upload_file": (
        "spells_phb.json",
        open(f"{data_root}/spells_phb.json", "rb"),
        "application/json",
    )
}
spells_phb_response = requests.post(
    url=f"{api_root}/spells/bulk", files=files, headers=headers
)
update_report(report, spells_phb_response, files.get("upload_file")[0])

files = {
    "upload_file": (
        "spells_xanathars.json",
        open(f"{data_root}/spells_xanathars.json", "rb"),
        "application/json",
    )
}
spells_xanathars_response = requests.post(
    url=f"{api_root}/spells/bulk", files=files, headers=headers
)
update_report(report, spells_xanathars_response, files.get("upload_file")[0])

files = {
    "upload_file": (
        "spells_tashas.json",
        open(f"{data_root}/spells_tashas.json", "rb"),
        "application/json",
    )
}
spells_tashas_response = requests.post(
    url=f"{api_root}/spells/bulk", files=files, headers=headers
)
update_report(report, spells_tashas_response, files.get("upload_file")[0])

################################################################################
# 4. SpellToClass
################################################################################
files = {
    "upload_file": (
        "spell_to_class_phb.json",
        open(f"{data_root}/spell_to_class_phb.json", "rb"),
        "application/json",
    )
}
spell_to_class_phb_response = requests.post(
    url=f"{api_root}/spell-to-class/bulk", files=files, headers=headers
)
update_report(report, spell_to_class_phb_response, files.get("upload_file")[0])

files = {
    "upload_file": (
        "spell_to_class_xanathars.json",
        open(f"{data_root}/spell_to_class_xanathars.json", "rb"),
        "application/json",
    )
}
spell_to_class_xanathars_response = requests.post(
    url=f"{api_root}/spell-to-class/bulk", files=files, headers=headers
)
update_report(report, spell_to_class_xanathars_response, files.get("upload_file")[0])

files = {
    "upload_file": (
        "spell_to_class_tashas.json",
        open(f"{data_root}/spell_to_class_tashas.json", "rb"),
        "application/json",
    )
}
spell_to_class_tashas_response = requests.post(
    url=f"{api_root}/spell-to-class/bulk", files=files, headers=headers
)
update_report(report, spell_to_class_tashas_response, files.get("upload_file")[0])

################################################################################
# 5. REPORT
################################################################################
print("REPORT: ", report)  # noqa: T001
