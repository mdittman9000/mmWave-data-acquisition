import random
from pathlib import Path

path = "data/"

imag_files = [path for path in Path('data').rglob('*.imsession')]
mode = 1




for i in range(len(imag_files)):
    ifile = open(imag_files[i], "w")

    rand_hash = hex(random.getrandbits(128))
        
    while(len(rand_hash) < 34):
        rand_hash = str(rand_hash) + '0'

    timeLineID = ("  <Timeline id=\"{}-{}-{}-{}-{}\">\n").format(rand_hash[2:10],rand_hash[10:14],rand_hash[14:18],rand_hash[18:22],rand_hash[22:34])

    dir = "\\".join(str(imag_files[i]).split('\\')[:-1])
    label_file = [path for path in Path(dir).rglob('*.label')]
    label_file = str(label_file[0]).split('\\')[-1]
    class_name = label_file.split('.')[0]

    if mode == 0:
        ifile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        ifile.write("<ImagimobStudio>\n")
        ifile.write(timeLineID)
        ifile.write("    <Tracks>\n")
        ifile.write("      <Track name=\"sampledVideo\" type=\"videomp4\">\n")
        ifile.write("        <PayloadFile>sampledVideo.mp4</PayloadFile>\n")
        ifile.write("      </Track>\n")
        ifile.write("      <Track name=\"sampledData\" type=\"datacsv\">\n")
        ifile.write("        <PayloadFile HasHeader=\"True\" DecimalPoint=\".\" FieldDelimiter=\",\">sampledData.csv</PayloadFile>\n")
        ifile.write("      </Track>\n")
        ifile.write("      <Track name=\"" + class_name +  "\" type=\"labelcsv\">\n")
        ifile.write("        <PayloadFile HasHeader=\"True\" DecimalPoint=\".\" FieldDelimiter=\",\" DurationColumnIndex=\"1\" TextColumnIndex=\"2\" ConfidenceColumnIndex=\"3\" CommentColumnIndex=\"4\" TimeColumnIndex=\"0\" TimeUnit=\"Seconds\" DurationUnit=\"Seconds\">" + label_file + "</PayloadFile>\n")
        ifile.write("      </Track>\n")
        ifile.write("    </Tracks>\n")
        ifile.write("  </Timeline>\n")
        ifile.write("</ImagimobStudio>\n")
    elif mode == 1:
        ifile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        ifile.write("<ImagimobStudio>\n")
        ifile.write(timeLineID)
        ifile.write("    <Tracks>\n")
        ifile.write("      <Track name=\"sampledVideo\" type=\"videomp4\">\n")
        ifile.write("        <PayloadFile>sampledVideo.mp4</PayloadFile>\n")
        ifile.write("      </Track>\n")
        ifile.write("      <Track name=\"rawData\" type=\"datacsv\">\n")
        ifile.write("        <PayloadFile HasHeader=\"True\" DecimalPoint=\".\" FieldDelimiter=\",\">adcExtractedData.csv</PayloadFile>\n")
        ifile.write("      </Track>\n")
        ifile.write("      <Track name=\"" + class_name +  "\" type=\"labelcsv\">\n")
        ifile.write("        <PayloadFile HasHeader=\"True\" DecimalPoint=\".\" FieldDelimiter=\",\" DurationColumnIndex=\"1\" TextColumnIndex=\"2\" ConfidenceColumnIndex=\"3\" CommentColumnIndex=\"4\" TimeColumnIndex=\"0\" TimeUnit=\"Seconds\" DurationUnit=\"Seconds\">" + label_file + "</PayloadFile>\n")
        ifile.write("      </Track>\n")
        ifile.write("    </Tracks>\n")
        ifile.write("  </Timeline>\n")
        ifile.write("</ImagimobStudio>\n")
    elif mode == 2:
        ifile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        ifile.write("<ImagimobStudio>\n")
        ifile.write(timeLineID)
        ifile.write("    <Tracks>\n")
        ifile.write("      <Track name=\"sampledVideo\" type=\"videomp4\">\n")
        ifile.write("        <PayloadFile>sampledVideo.mp4</PayloadFile>\n")
        ifile.write("      </Track>\n")
        ifile.write("      <Track name=\"fullData\" type=\"datacsv\">\n")
        ifile.write("        <PayloadFile HasHeader=\"True\" DecimalPoint=\".\" FieldDelimiter=\",\">fullData.csv</PayloadFile>\n")
        ifile.write("      </Track>\n")
        ifile.write("      <Track name=\"" + class_name +  "\" type=\"labelcsv\">\n")
        ifile.write("        <PayloadFile HasHeader=\"True\" DecimalPoint=\".\" FieldDelimiter=\",\" DurationColumnIndex=\"1\" TextColumnIndex=\"2\" ConfidenceColumnIndex=\"3\" CommentColumnIndex=\"4\" TimeColumnIndex=\"0\" TimeUnit=\"Seconds\" DurationUnit=\"Seconds\">" + label_file + "</PayloadFile>\n")
        ifile.write("      </Track>\n")
        ifile.write("    </Tracks>\n")
        ifile.write("  </Timeline>\n")
        ifile.write("</ImagimobStudio>\n")


    ifile.close()
    