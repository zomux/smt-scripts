import sys, os

if len(sys.argv) != 3:
  print "python zero-bleu.py [result] [reference]"
  raise SystemExit

_, pathResult, pathRef = sys.argv

def listLineBleu(pathResult, pathRef):
  resultLineBleus = os.popen("ruby ~/apps/bleu_kit/line_bleu.rb %s %s" % (pathResult, pathRef)).read().strip()
  lineBleus = resultLineBleus.split("\n")
  return [float(l.split("\t")[0]) for l in lineBleus]



listBleus = listLineBleu(pathResult, pathRef)

# Count zero bleu lines.
print "Bleu=0 lines:", listBleus.count(0.0)

# Count for ranged length.

pathEn = pathRef.replace(".ja", ".en").replace(".ref", ".src")
linesEn = open(pathEn).read().strip().split("\n")
linesRef = open(pathRef).read().strip().split("\n")
linesResult = open(pathResult).read().strip().split("\n")
linesCompare, pathCompare = None, ""
if "moses." in pathResult:
  pathCompare = pathResult.replace("moses.", "gentile.")
elif "gentile." in pathResult:
  pathCompare = pathResult.replace("gentile.", "moses.")

if os.path.exists(pathCompare):
  linesCompare = open(pathCompare).read().strip().split("\n")

mapLengthBleuSum, mapLengthCount = {}, {}
for iLine, lineEn in enumerate(linesEn):
  bleu = listBleus[iLine]
  if bleu == 0 :
    print "[E]", linesEn[iLine]
    print "[J]", linesRef[iLine]
    print "[R]", linesResult[iLine]
    if linesCompare:
      print "[C]", linesCompare[iLine]
    print "---"
