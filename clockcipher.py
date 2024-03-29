import random

elScores = {'E': 12.02,
            'T': 9.1,
            'A': 8.12,
            'O': 7.68,
            'I': 7.31,
            'N': 6.95,
            'S': 6.28,
            'R': 6.02,
            'H': 5.92,
            'D': 4.32,
            'L': 3.98,
            'U': 2.88,
            'C': 2.71,
            'M': 2.61,
            'F': 2.3,
            'Y': 2.11,
            'W': 2.09,
            'G': 2.03,
            'P': 1.82,
            'B': 1.49,
            'V': 1.11,
            'K': 0.69,
            'X': 0.17,
            'Q': 0.11,
            'J': 0.1,
            'Z': 0.07}

alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
mainText = '''VXLKV ZXZSZ XODRQ YFQEM OLMRT OFATI MXTAW AYANK RBPCE SXCUP OB#RT BXSEK RDSJ+ WYTG+ JDIKP NRJTP #AFYX 
BAZRO VAWUH RUYIZ RCOSX CBNW# VNIQS XJPEU YKCJO PSMCE QXBIC #HYIZ T+RBJ +MXPM TDSKR UNQ#U BIHZX VBZET EGSZE MWXQD 
UFQXS EKRZD ENOND SZEQU IXNGL +REON AHUOQ +ULFN ELDQB HKZGS QPSMC NRQ#O LMEOP FXLBU LSY#I C+IO# SGRDL VIMFU MPOTL 
UPADT SCAUW MSJGX VHWAH CIWBN KAPIZ EMWPX DBLCP +H#KN RJTPZ ELNZA WZRKS HKNDS LHJNK VFQHM O#ATL SPISE JFSTD SPQYQ 
FQEGZ HLNDX Z+VKB +JKSD FWZAT UXH#K M#XNH XHZTL UKBTE BWDPU #APXB POTGZ CHODT SQGNB J#IVU VMZXV +PFAN TRILP EMHYO 
ERKAR T+YDJ WOIHU IZFTX LWUB+ ZGSLN QYT+R +THCH TPBXZ JVLDT EIWIH KNDA# IQYCL WJVMO PWRFT GKXCQ EHCNH MBEQ+ MPUCO 
DSOLD JWKSH KNDA# ILUXV TOCHC KUVQR FBXJT AZAKU FHIYT BJNMC HSOXL XYJKM ZJWMD UGNWP BWYRX ISFUL YNTBZ WZKTY GRY+R 
QVH#S W#QBF YXW+W ZSIAS TI+VR GPXQM XEVUK QXJGN IXBGH EWYIY WYSXB L+JWG ZCHOQ HZWLX QBHVJ ZSDKW RGFTU GXTGW #MEOT 
NTEJA QH#JE AJWRQ GVKYX N#LOZ WUZTW PHWXB MPT+D LVZXJ HIONA TEUQO SRDLW YR+CP VQENQ MENKX Z+UBX KSMTO JWMI+ SUJND 
JMXI# HPMEO WUXYJ ZXJPM IKRZI QCXBO #HYAI FDUVQ KUBNH YVHWP RBTCJ +MPOR QVNEG IVXYJ KCRUI ZQDIH PJVLU IVGJB VXYWS 
QNH#V YQCJP VMGOQ FMNCK XFLDT SGRAS RHWC# FOFAV LNBIF HNELJ BNHYE MIAPS MCJPY IWQJH VCWDU RFBRT BNBJA UKW+A SVCND 
JM+BP M#PLJ HLNVZ LUPAX PR+HN LR+DI VHGPA SPBNU HFOIH PZTYX NS+QA #VD+B PHGLE QROFX QRNYD FSFJO IXAI+ QEIEM EOTXL 
NJBZW SGSFA XUOQF P+MQP HULTE GHPZT HBJKT KVNHM BEQEI EKVUS EFLPJ HOK#T DIARY FQPBO CPOWS ROENQ IJ+WC JZTRW OAX+Y 
FQPBO CPOW# ANPIX ALTVW KSHXQ MCENG MEOHU QPXBE ROCKC R+VQS PIVNQ LBAIN WILDT #DRHK OXWDR XIWCP CUCPC UFYJB WHQXY 
PER+G A#INQ PBOCP OWHZT XTPZM WYWSV JA#YF QSH#X EUOCJ FULRO EILZI JZXOD HOAX+ WMT+Z QG+SR UGPQH RNLDT CRNIS RYTDL 
VGWXH #SCKU NENUK TJKPA WIXJS V#KME N#TQW IXBJ+ WKJWO XMDLG VPWKC KUENU IPGJR WMKNP RDHWD LPBOC POW#J QTEGB +EJSH 
WAYTQ YCLWA HVLSO RSUZX NJ+BT ESGRA SRXMQ X+SCT PMULN YDHFO VKSYC JDRQN FYFW+ DHXVH WLYWY QLXYJ ZXJEQ UI+LX MQSI# 
XMHCT OB#TY H#NIX JHY#H #NYI# V+IVG ZCHOW #QBTI LDTGN EVZDS JLHIJ MINR+ UIFLJ M#OWR FYX+Z SOJPU KCQYD LVTZW OQTNC 
UQDLD TVJWU +LQFP GQPXV BZDHR FVBLB +JPVY DXDYW MISVW APCJS CILJH FYLDT ZGXK# SZDMX UWTC+ BPECU IOWAQ WKGCQ SNDSA 
WOHMY WMIRC +BPMR CNZDU RFBRT BNHYO CKCRY TOQGX KXMCK PWRNQ RXKJT IXD+N ITRUW DQPFP U#NBN UTEGZ TSODH KYHIY WTCBO 
CAH#C IXNXV HEYXP MHKND A#IZQ #HUXV CKNAT BNTZG KSWQM UTRCP MPUSO W#ANK UOTYX MUNLY FP+TW BYPUL RSOKA +WZSI YDWYQ 
ESFJV COPB# HVNLP CTSRP SCASG YFQ+B IMKYB NW#HZ XBXSV XYJRN GLUXI SFULY ZIWRV +HPZS YJPEU YJFSY WNMST JVDZU FVTAN 
O#EMW AXHI+ RCHE+ OFOHR A#ANG XHPYX ETU+A XRQ+W SMPAH CNPZU +OPJN TVOCK CRVI+ RHFOF ANQLE O+UTE SXKWP JADPD LV#GZ 
QJSKI SE+MX SZESN YKWL# XHIYQ GIEME OFUHR TESNI SECAK SHW+I RYFQC #SMQJ QSWAQ WKGCT ZWNSD J+A#S U+QIH MKJMR FTOQS 
RFKXS BJXEK NVXOD JEVGP CIPBU FYXHP QBTGM SRASA IDPGQ PMSAI F#ANV ZXZSZ XODLH YDLVK PRWBP #HQEH IVZGR YDRGU WJU#+ 
H#PWT SZTXF TKAQN ZJPCU AKVNY RVNJ# TJMRF APFW# HZQL+ NBLPE ZTBJY EUPYR GIJHB GSRAV SFSBF OENB+ JOASA IASXM TCPVG 
ZHXFU TKUQT IGRKJ O#VGM V#QFP SCILW UXVKM IJUVH KGRVY QCJES XAMCK XFLDU QRSVW YRWKN FHV+N DJM+B PCHVS NFHRH LDSZE 
MWBDW DRXBV WGH#B VNELH SREAQ AXDIP VLH#O HORQV Q+JBN HYQTK CA#IL ULGVM KQGVY PBOFY XRHED #LWAP RIMDL VIMKN VLHUV 
BOBXS ACOVA HMHUY VNR+I TAWCL SCIL# ANVKY RQRQA XIMNU GVGZU CTONT ELZIY RPVYD MVMD+ BPRVS CIDLT WB+JU TDKNQ HV+DL 
VUHUL BI#JH ZTEGB +NVAK UMRQD OR#FA PMEOL FQ#VT SZXOD KCQYI MNUGV TGZUC #AHRS OKA+W AYW+O AX+YF QMFOF LPBO+ OFUQN 
HYMIO LRYI+ SI#PA CKXFA JKISE RMXKP EQT+G BRYFQ JM+IW OLFVH K#YQL FYXSZ ERWXI OSYQT RCPIK PJXVC KXZNW HPHYP EUYKC 
RPNUI QPJMC KXFJV RQKDT KJ+AX YHTDQ HWTGW UC#XN PFYXT CUVDF OAIVW NDJGH #KONB US+VK QNZJP UYW+S GRPVJ GMQAR #NZIZ 
ULDTZ GRNWO FXDTU GZSMG ZORQH ZUJUZ EWX#H OAX+Y FQXNC #R#C# UTPIQ +HQD# HWAH+ CTJRS XMFIW #RTLB +JERA SRYNR CHE+O 
FOHRA #ANJB ZWSNP UKCQY PTUVH #RWLP #QLUR JZMOH BJUSD KOQGB JPWVO EQFUB NWRNI QOJYE U#A#I NQPXC VCXW# QBDVA YHIXY 
JKCRX +I+P+ ISFME OWX+Q FTUXB TWUPH CNHMB +QCEV YGRJW #QUXB +JKQT KCA#I NUMCW CMCOX VRTLB +JGON WNFYF Q#JPO LWCMS 
HFSBZ XJ+NJ MXYPU PA#TV CZJ#T GW#UJ DIXFS OKAQB SACFQ AX+WV WOSXO LBJLX FLDZT JMOKE IHWKR G#PCN HMUJH UIZ+W UB+WM 
R+GBV QS+QC EVYGR JWQDV KTZGX KESW+ NGYFQ +BIMG PHLCK JANEL DTVJR ARCO# XOCZL H+PAV OD+VW KQBHK ROVQT +G+RI Z+SVU 
VLNUN URILP SCHWE WIDQB MITBP OC#XP BOJVR JAYHQ EKNTI Q+IGJ MRFCK ULNJZ TBJKI NI+VF SUFWM IDVTJ HBSPB #AHRE XUX+# 
OVACN XBPCE NPCHU IVPXK MVZJR +J+WX MQHZG PCMEO ILULT LUPAV ZOATK XSRFD BVPLB OWRIX JQKSK CQYTE +HI#Q FPRBU HZT+F 
JKJT+ HIJZS AVWXH UYBTQ DVMUM EVLHJ UXJKB HKEJZ SDKOH UGRPI SFVLN YCXZX NV+B+ JOASA IASXM NDJMI EMEVS QHRIU PAVQS 
WSWLU YFQCI GNQLB DOIZK SJHSZ ESANF BPOTA PEWCH CKUST BMXNU KQSAC IUPYA #DIQP SRCUA HSPBE QEGPA IXD+Y GQPVQ +UVRH 
FMWBO PBNQV BGUKS ZXYJU PYSGY IC#IV HLUOU YDVBL QCT+N ACJYS NQGSG INX+S CNPZU MO+UN EWJBJ +NATR DFGSU YIMRC QHU#O 
ASEKS +PZQN TYPEM IAYFQ JMVMO MVRBN QWKGD SBJFS W+IXJ G+JWQ JHYXZ +JQSE JPV+K NFYFT NQV#J XQCVO WJUAT FXMNV SOZSA 
WLVMQ UGW#J HUFUF TUXKJ RNYOQ DU+MP ZH+BP UO#IZ JPMPQ VPEUY VWCQA IEQV# XFUYB O#QOE +UABE WESKC JOWDT UMKXM VCPWP 
ZQSEL DSZEM WGRVB I+RXT WIOIZ NWUB+ ZGSTD JASVC LH#KM EN#FY XWSEJ ERXJ+ WYFQ# VOKWL SPOZT KIUKB TYDTS RGQIN DJM+B 
PZHNY IYFYX JHQYE SAJ+A RMCRQ PFOHD FXZXY RQTVZ GSRNL RGVJQ MVOCB NBDSN WUAY# JURXJ +WIYQ GOVZE WCMCI DHRXV FXZ+J 
KTFW+ ASYPN DJMUB IFPME ODUXK JZSZX ODU#P QDVMZ +BPAH SCFSN FOVKP GZGSA F#OVU YIJPG VGZHU OB#LT KNPSY VOCKC JOX+I 
+P+IS FMEOZ IZ+VK BEXRD SGRHW C#KVR PNCIU ZRWBU KXWMD OQU#C JW#NO VCR+O I#GPL BPONE TXBHX YCUAX NHDZP +GLHF ZXZRI 
LPERN ZGOVK A#IW+ VJWRT LPNTL UPAVI JQT+G BROMP E#VGW IRBHF VBMZN ZXPMY GQGUG #HPI# VPOFV TEANB JPRKP +GIVQ XTOCN 
#PWPR FVZUG ZGSAW JOQGP QFPCP VGZUC QUVGN BIPGR OVASY XOGVJ NFKYH UXBFW BXMWY #TDKW YDTIH GPACK UZJVR Q+HQD #ILQG 
BTC+B PJUYR CNHUQ BNBJB NHYRD FYRYO +C+SG QCFP# GWDXZ QBHKA KUKWI YWMI+ BPQAH LCP#T QDLDT ZKTI+ WMIWN JZEU# HFUTL 
XZYHY JKWYT WJGJG +H#HP MRJWR FVZWX JWYCT DFNA# I+OPO TGW#C RMIPN LDTIW KFPAP RHTU# EZI#K QMIR# ODHD+ UJQDE KNRGU 
O+Q+B OMXHU XZSOE UBRNZ GOVKI +RYHT +WJZO VHLCW HZFYX JWATK IGOAX +YFQS ITJVR BJHEK MXZTX WK#SF QUVNU VPVTJ RBEJO 
+RTSR DSHQD VMDQV GZHV# SNAUF JILPE BHXYW AWQUI DLVTP OJFHF JV+B+ JDODF NGY+R H#VLH VCPWN LWXOJ AB+WE KCRQC TVWPI 
CZH#Y OCHXN JKMZG SIOUT VRHGP AUIDU GVPUV KSIRC NHDCT CESFU POB#R ILPEB +J#SE JIRQP C#SGA PUBZI JU+LP GWD+J +AXIM 
QSOBO FASNB DFYOI HIVZ# JEMWA X+G+R JGIGU JMRFP YJVRJ ZTSRY KPYRB DLV#G ZHUID UGVPU SODKI J+SGR DLVRP NSCI# ANTUE 
+JKNP OABRB INDGS UPASC ILHFO IEZNA ZJ#U+ O+IVR HFCO# H#CKX FIDPI YCJRH JGVLS UNJF+ PYJ#H FXJKS YVOFS TDSRU YIZRZ 
#POHS WXLJI LPER+ JYVHJ +WYFQ SHPBI #PMUQ ONTBX BHJKR HWA#I VRMBP CUBFK X+UFT DLXZI VJRDF AXBIC Q+VGZ HQOTY LVHB+ 
JWUFW BXTW+ SPFJT #O#AT LKPHY SPORU YFQXH WPIHX #JHXN ILPEB +NVIX D+IGO XDIZN PVGZH #PWPQ DLDTU JISFI S+FQG ZOLBP 
BOHZF VXKTO RGRDF OUYTG RZHUF CJFUT ZETWK PTNXS GIMD+ BPFTS OIZNV +B+JP MIDRB VLHMV HSCID URFBP WZGSF WKSQI G+QBV 
MOALN YJFTH ZUOLB HTSKC RDHWD L+BPO ENFON LPNAS KSIOR YFQEV TGCTO CPCUB VWXZS ACURX WJA#V +ZQG+ SMPOR BW#LW XLQBH 
KJZSA QNGIW MDLVW S+PRH LCTPZ EGNZB JWNAT CUAQN HDUOQ VQXTO FAXIS LXVRZ SXJRD FIXJS IGRHL C#QFY X+SZG SAGQG BOR#F 
AP#CU VSODY QLNFX ZQBHK ROVRA WQGWM NMIMO MVRB# QWIJA YVZOA QTHCJ +WPTU #NPRQ FMEOA PBXEB YJQTH MEMWN DRDVD RJ#TG 
W#NRJ FWSZX KXRNY GS+N '''
mainText = mainText.replace(' ', '').replace('\n', '')


def mutate(key):
    ans = list(key)
    for _ in range(5):
        i = list(range(len(key)))
        random.shuffle(i)
        p1, p2 = i[:2]
        ans[p1], ans[p2] = ans[p2], ans[p1]
    return ''.join(ans)


def score(k):
    text = decrypt(mainText, k)
    ans = 0
    for letter in text:
        if letter == '6':
            return 0
        else:
            ans += elScores[letter]**2
    return ans


def decryptOld(text, key, alphabet=alph):
    ans = ''
    for n, l in enumerate(text):
        pos = len(alphabet)*(n+1)
        pos //= len(key)
        pos *= len(key)
        pos += key.find(l)

        ans += alphabet[pos % len(alphabet)]
    return ans


def decrypt(text, key, alphabetLength=26):
    # alphabetLength must be < keylength
    keylength = len(key)
    disp = 0
    diff = keylength - alphabetLength
    ans = ""
    prevKeyPos = -1  # ensures keyPos !<= prevKeyPos for first letter
    for n in text:
        keyPos = key.index(n)
        if keyPos <= prevKeyPos:
            disp += diff
            if disp >= alphabetLength:
                disp -= alphabetLength
        ans += alph[(keyPos + disp) % alphabetLength]
        prevKeyPos = keyPos
    return ans


populationSize = 50
baseKey = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ+#')
population = []
for _ in range(populationSize):
    random.shuffle(baseKey)
    population.append(''.join(baseKey))

genNo = 0
while True:
    population = population + [mutate(x) for x in population]
    population.sort(key=score, reverse=True)
    population = population[:populationSize]

    print(genNo, score(population[0]), population[0], decrypt(mainText, key=population[0])[:110])

    genNo += 1
