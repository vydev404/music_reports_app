# -*- coding: utf-8 -*-
class ReportsGenerator:
    def __init__(self, report_template: Path, reports_dir: Path):
        self.report_template = report_template
        self.reports_dir = reports_dir

    def generate_report(self, source_file: FileData) -> ReportData:
        report_file = self.reports_dir / f"{source_file.name}.xlsx"
        report_file = self.rename_if_exists(report_file)
        report = ReportData(report_name=source_file.name, source_file=source_file.file_id, report_file=report_file)

        header_data = {
        'C3': source_file.name,
        'C4': source_file.created,
        'C5': source_file.parsed_data.timecode,
        'C6': 0,
        }

        wb = openpyxl.load_workbook(self.report_template)

        ws = wb.active

        clips = source_file.parsed_data.data.get("clips_in_db", [])

        for row_num, clip in enumerate(clips, start=10):
            if not isinstance(clip, FormatedClipData):

                continue
            header_data['C6']+= clip.duration_in_frames
            ws.cell(row=row_num, column=1, value=row_num - 9)
            ws.cell(row=row_num, column=2, value=clip.file_info.track_name if clip.file_info else "N/A")
            ws.cell(row=row_num, column=3, value=f"{clip.file_info.artist if clip.file_info else ''}")
            ws.cell(row=row_num, column=4, value=clip.file_info.album if clip.file_info else "N/A")
            ws.cell(row=row_num, column=5, value=clip.duration_in_tc)
            ws.cell(row=row_num, column=6, value=source_file.name)
            ws.cell(row=row_num, column=7, value=clip.file_info.right_holder if clip.file_info else "N/A")

        header_data['C6'] = tc.frames_to_timecode(header_data['C6'])
        for k, v in header_data.items():
            ws[k].value = v
        wb.save(report.report_file)

        return report

    def generate_not_in_db_list(self, source_file: FileData):
        clips = source_file.parsed_data.data.get("clips_not_in_db", [])
        not_included = self.reports_dir / f"{source_file.name}_not_in_db.txt"
        if not clips:
            return
        with open(not_included, "w", encoding="utf-8") as f:
            header = f"[*]  PARSED CLIP FILES FROM {source_file.full_name} NOT FOUNDED IN DATABASE\n\n"
            f.write(header)
            for i, clip in enumerate(clips, start=1):
                f.write(f"[{i:02}] {clip.clip_name: ^70}| used: {clip.count: ^3} times | total duration: {clip.duration_in_tc: ^9}\n")


    @staticmethod
    def rename_if_exists(file: Path)-> Path:
        count = 1
        tmp = file
        while tmp.exists():
            tmp = f"{file.stem}_{count:02}{file.suffix}"
            count += 1
        return tmp