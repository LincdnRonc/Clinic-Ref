# eviQ radiation oncology protocol links per page (links only; no eviQ content is reproduced).
# Each entry: (protocol ID or '', title, URL). Category links point to eviQ's listing pages.
B = 'https://www.eviq.org.au/radiation-oncology/'
CAT = 'https://www.eviq.org.au/Radiation-oncology/'

def p(path):
    return B + path

EVIQ = {
 'breast-early.html': [
  ('1921', 'Breast DCIS adjuvant EBRT', p('breast/1921-breast-ductal-carcinoma-in-situ-adjuvant-ebrt')),
  ('3650', 'Breast invasive cancer adjuvant whole breast EBRT', p('breast/3650-breast-invasive-cancer-adjuvant-whole-breast')),
  ('3658', 'Breast invasive cancer/DCIS adjuvant partial breast EBRT', p('breast/3658-breast-invasive-cancer-ductal-carcinoma-in-si')),
  ('', 'All eviQ breast radiation oncology protocols', CAT + 'Breast'),
 ],
 'breast-nodes-pmrt.html': [
  ('1924', 'Breast invasive cancer adjuvant nodal irradiation EBRT', p('breast/1924-breast-invasive-cancer-adjuvant-nodal-irradia')),
  ('1925', 'Breast invasive cancer adjuvant EBRT post-mastectomy', p('breast/1925-breast-invasive-cancer-adjuvant-ebrt-post-mas')),
  ('1926', 'Breast inflammatory cancer adjuvant/neoadjuvant EBRT', p('breast/1926-breast-inflammatory-cancer-adjuvant-neoadjuva')),
  ('', 'All eviQ breast radiation oncology protocols', CAT + 'Breast'),
 ],
 'breast-planning.html': [
  ('3650', 'Breast invasive cancer adjuvant whole breast EBRT', p('breast/3650-breast-invasive-cancer-adjuvant-whole-breast')),
  ('1925', 'Breast invasive cancer adjuvant EBRT post-mastectomy', p('breast/1925-breast-invasive-cancer-adjuvant-ebrt-post-mas')),
  ('', 'All eviQ breast radiation oncology protocols', CAT + 'Breast'),
 ],
 'thorax-early.html': [
  ('3389', 'NSCLC definitive stereotactic EBRT peripheral tumours', p('respiratory/3389-respiratory-non-small-cell-lung-cancer-defini')),
  ('4018', 'NSCLC definitive stereotactic EBRT central tumours', p('respiratory/4018-respiratory-non-small-cell-lung-cancer-defini')),
  ('3697', 'NSCLC definitive EBRT hypofractionation', p('respiratory/3697-respiratory-non-small-cell-lung-cancer-defini')),
  ('', 'All eviQ respiratory radiation oncology protocols', CAT + 'Respiratory'),
 ],
 'thorax-stage3.html': [
  ('1871', 'NSCLC definitive EBRT with or without chemotherapy', p('respiratory/1871-respiratory-non-small-cell-lung-cancer-defini')),
  ('3697', 'NSCLC definitive EBRT hypofractionation', p('respiratory/3697-respiratory-non-small-cell-lung-cancer-defini')),
  ('1873', 'NSCLC adjuvant EBRT post-operative', p('respiratory/1873-respiratory-non-small-cell-lung-cancer-adjuva')),
  ('1880', 'NSCLC superior sulcus (Pancoast) neoadjuvant chemoradiation', p('respiratory/1880-respiratory-nsclc-superior-sulcus-pancoast')),
  ('1872', 'Lung primary palliative EBRT', p('respiratory/1872-respiratory-lung-primary-palliative-ebrt')),
 ],
 'thorax-sclc.html': [
  ('4292', 'Small cell lung cancer thoracic EBRT with or without chemotherapy', p('respiratory/4292-respiratory-small-cell-lung-cancer-thoracic-e')),
  ('3679', 'Small cell lung cancer consolidative EBRT', p('respiratory/3679-respiratory-small-cell-lung-cancer-consolidat')),
  ('', 'All eviQ respiratory radiation oncology protocols', CAT + 'Respiratory'),
 ],
 'thorax-other.html': [
  ('', 'All eviQ respiratory radiation oncology protocols', CAT + 'Respiratory'),
 ],
 'hn-general.html': [
  ('3390', 'Head and neck SCC adjuvant EBRT post-operative ± chemotherapy', p('head-and-neck/3390-head-and-neck-squamous-cell-carcinoma-adjuvan')),
  ('4399', 'Head and neck palliative EBRT', p('head-and-neck/4399-head-and-neck-palliative-ebrt')),
  ('', 'All eviQ head and neck radiation oncology protocols', CAT + 'Head-and-neck'),
 ],
 'hn-oropharynx.html': [
  ('3390', 'Head and neck SCC adjuvant EBRT post-operative ± chemotherapy', p('head-and-neck/3390-head-and-neck-squamous-cell-carcinoma-adjuvan')),
  ('', 'All eviQ head and neck radiation oncology protocols (oropharynx protocols recently revised)', CAT + 'Head-and-neck'),
 ],
 'hn-larynx.html': [
  ('4356', 'Larynx/hypopharynx SCC definitive EBRT ± chemotherapy', p('head-and-neck/4356-head-and-neck-larynx-hypopharynx-scc-definiti')),
  ('', 'All eviQ head and neck protocols (including glottic larynx definitive EBRT)', CAT + 'Head-and-neck'),
 ],
 'hn-oral-salivary.html': [
  ('756', 'Major salivary gland adjuvant EBRT post-operative high risk', p('head-and-neck/756-head-and-neck-major-salivary-gland-primary-a')),
  ('3390', 'Head and neck SCC adjuvant EBRT post-operative ± chemotherapy', p('head-and-neck/3390-head-and-neck-squamous-cell-carcinoma-adjuvan')),
  ('', 'All eviQ head and neck protocols (including oral cavity definitive EBRT)', CAT + 'Head-and-neck'),
 ],
 'hn-npc-sinonasal.html': [
  ('635', 'Nasopharynx definitive EBRT early-stage', p('head-and-neck/635-head-and-neck-nasopharynx-definitive-ebrt-earl')),
  ('621', 'Nasopharynx definitive EBRT chemoradiation', p('head-and-neck/621-head-and-neck-nasopharynx-definitive-ebrt-chem')),
  ('3888', 'Nasopharynx EBRT chemoradiation post-induction', p('head-and-neck/3888-head-and-neck-nasopharynx-adjuvant-ebrt-chemo')),
  ('1527', 'Paranasal sinus and nasal cavity adjuvant EBRT', p('head-and-neck/1527-head-and-neck-paranasal-sinus-and-nasal-cavit')),
 ],
 'hn-thyroid-cup.html': [
  ('', 'All eviQ head and neck radiation oncology protocols', CAT + 'Head-and-neck'),
 ],
 'skin.html': [
  ('', 'All eviQ skin radiation oncology protocols', CAT + 'Skin'),
 ],
 'cns-glioma.html': [
  ('409', 'Glioblastoma (IDH-wildtype) EBRT chemoradiation', p('neurological/409-brain-adult-glioma-cns-who-grade-4-glioblastom')),
  ('410', 'Grade 3–4 astrocytoma or glioblastoma EBRT short-course', p('neurological/410-brain-adult-glioma-cns-who-grade-3-4-astrocyto')),
  ('1621', 'Grade 3–4 astrocytoma or grade 3 oligodendroglioma (IDH-mutant) EBRT', p('neurological/1621-brain-high-grade-anaplastic-glioma-adjuvant-e')),
  ('', 'All eviQ neurological radiation oncology protocols', CAT + 'Neurological'),
 ],
 'cns-benign.html': [
  ('', 'All eviQ neurological radiation oncology protocols', CAT + 'Neurological'),
  ('', 'All eviQ stereotactic protocols', CAT + 'Stereotactic'),
 ],
 'cns-general.html': [
  ('', 'All eviQ neurological radiation oncology protocols', CAT + 'Neurological'),
 ],
 'heme-hodgkin.html': [
  ('3619', 'Hodgkin lymphoma early-stage EBRT to involved sites', p('haematology/3619-hodgkin-lymphoma-early-stage-ebrt-to-involved')),
  ('', 'All eviQ haematology radiation oncology protocols', CAT + 'Haematology'),
 ],
 'heme-nhl.html': [
  ('1804', 'DLBCL limited-stage EBRT to involved sites', p('haematology/1804-non-hodgkin-diffuse-large-b-cell-lymphoma-lim')),
  ('3608', 'Follicular lymphoma definitive EBRT', p('haematology/3608-non-hodgkin-follicular-lymphoma-definitive-eb')),
  ('', 'All eviQ haematology radiation oncology protocols', CAT + 'Haematology'),
 ],
 'heme-other.html': [
  ('4401', 'Primary cutaneous T-cell lymphoma definitive or palliative EBRT', p('haematology/4401-non-hodgkin-primary-cutaneous-t-cell-lymphoma')),
  ('4617', 'Primary cutaneous T-cell lymphoma total skin electron therapy', p('haematology/4617-non-hodgkin-primary-cutaneous-t-cell-lymphoma')),
  ('', 'All eviQ haematology radiation oncology protocols', CAT + 'Haematology'),
 ],
 'pall-brain.html': [
  ('3253', 'Brain metastases stereotactic', p('palliative/3253-brain-metastases-palliative-ebrt-stereotactic')),
  ('3572', 'Brain metastases stereotactic post-operative', p('palliative/3572-brain-metastases-palliative-ebrt-stereotactic')),
  ('3882', 'Brain metastases hippocampal avoidance whole brain', p('palliative/3882-palliative-brain-metastases-ebrt-hippocampal')),
  ('1251', 'Brain metastases whole brain', p('palliative/1251-brain-metastases-palliative-ebrt-whole-brain')),
 ],
 'pall-bone-spine.html': [
  ('268', 'Bone metastases palliative EBRT', p('palliative/268-palliative-bone-metastases-ebrt')),
  ('296', 'Spinal cord compression palliative EBRT', p('palliative/296-palliative-spinal-cord-compression-ebrt')),
  ('4098', 'Spinal bone metastases stereotactic', p('palliative/4098-spinal-bone-metastases-palliative-ebrt-stereo')),
  ('4099', 'Non-spine bone metastases stereotactic', p('palliative/4099-non-spine-bone-metastases-palliative-ebrt-ste')),
 ],
 'pall-oligo.html': [
  ('4026', 'Hepatic metastases stereotactic EBRT', p('upper-gastrointestinal/4026-hepatic-metastases-stereotactic-ebrt')),
  ('1872', 'Lung primary palliative EBRT', p('respiratory/1872-respiratory-lung-primary-palliative-ebrt')),
  ('4399', 'Head and neck palliative EBRT', p('head-and-neck/4399-head-and-neck-palliative-ebrt')),
  ('1026', 'Bladder carcinoma palliative EBRT', p('urogenital/bladder/1026-bladder-carcinoma-palliative-ebrt')),
  ('', 'All eviQ palliative and stereotactic protocols', CAT + 'Palliative'),
 ],
 'gu-prostate.html': [
  ('234', 'Prostate definitive EBRT intermediate-risk', p('urogenital/prostate/234-prostate-adenocarcinoma-definitive-ebrt-interm')),
  ('235', 'Prostate definitive EBRT high-risk', p('urogenital/prostate/235-prostate-adenocarcinoma-definitive-ebrt-high-r')),
  ('3657', 'Prostate definitive EBRT prostate and pelvic lymph nodes', p('urogenital/prostate/3657-prostate-adenocarcinoma-definitive-ebrt-prost')),
  ('4140', 'Prostate definitive ultra-hypofractionated stereotactic EBRT', p('urogenital/prostate/4140-prostate-adenocarcinoma-definitive-ultra-hypo')),
  ('415', 'Prostate HDR brachytherapy boost', p('urogenital/prostate/415-prostate-adenocarcinoma-definitive-hdr-brachy')),
  ('416', 'Prostate LDR brachytherapy (seeds)', p('urogenital/prostate/416-prostate-adenocarcinoma-definitive-ldr-brachyt')),
  ('4487', 'Prostate bed salvage or adjuvant EBRT', p('urogenital/prostate/4487-prostate-adenocarcinoma-prostate-bed-salvage')),
  ('3659', 'Prostate palliative EBRT low-volume metastatic disease', p('urogenital/prostate/3659-prostate-adenocarcinoma-palliative-ebrt-low-v')),
 ],
 'gu-bladder.html': [
  ('1025', 'Bladder carcinoma definitive EBRT ± chemotherapy', p('urogenital/bladder/1025-bladder-carcinoma-definitive-ebrt-with-or-wit')),
  ('1026', 'Bladder carcinoma palliative EBRT', p('urogenital/bladder/1026-bladder-carcinoma-palliative-ebrt')),
 ],
 'gu-kidney.html': [
  ('', 'eviQ kidney and adrenal radiation oncology protocols', CAT + 'Urogenital/Kidney-and-adrenal'),
 ],
 'gu-testis.html': [
  ('', 'All eviQ urogenital radiation oncology protocols', CAT + 'Urogenital'),
 ],
 'gu-other.html': [
  ('', 'All eviQ urogenital radiation oncology protocols', CAT + 'Urogenital'),
 ],
 'gi-oesophagus-gastric.html': [
  ('1861', 'Oesophageal neoadjuvant EBRT chemoradiation', p('upper-gastrointestinal/1861-oesophageal-neoadjuvant-ebrt-chemoradiation')),
  ('1865', 'Oesophageal definitive EBRT chemoradiation', p('upper-gastrointestinal/1865-oesophageal-definitive-ebrt-chemoradiation')),
  ('', 'All eviQ upper GI radiation oncology protocols', CAT + 'Upper-gastrointestinal'),
 ],
 'gi-pancreas.html': [
  ('3581', 'Pancreas definitive/neoadjuvant EBRT chemoradiation', p('upper-gastrointestinal/3581-pancreas-definitive-neoadjuvant-ebrt-chemorad')),
  ('', 'All eviQ upper GI radiation oncology protocols', CAT + 'Upper-gastrointestinal'),
 ],
 'gi-hepatobiliary.html': [
  ('4024', 'Hepatic primary (HCC, intrahepatic cholangiocarcinoma) stereotactic EBRT', p('upper-gastrointestinal/4024-hepatic-primary-stereotactic-ebrt')),
  ('4026', 'Hepatic metastases stereotactic EBRT', p('upper-gastrointestinal/4026-hepatic-metastases-stereotactic-ebrt')),
 ],
 'gi-rectum-colon.html': [
  ('1863', 'Rectal neoadjuvant chemoradiation long-course', p('colorectal/1863-rectal-neoadjuvant-ebrt-chemoradiation-pre-op')),
  ('1874', 'Rectal neoadjuvant EBRT short-course', p('colorectal/1874-colorectal-rectum-neoadjuvant-ebrt-pre-operat')),
  ('', 'All eviQ colorectal radiation oncology protocols', CAT + 'Colorectal'),
 ],
 'gi-anal.html': [
  ('1860', 'Anal definitive EBRT chemoradiation', p('colorectal/1860-anal-definitive-ebrt-chemoradiation')),
 ],
 'gi-general.html': [
  ('', 'All eviQ upper GI radiation oncology protocols', CAT + 'Upper-gastrointestinal'),
  ('', 'All eviQ colorectal radiation oncology protocols', CAT + 'Colorectal'),
 ],
 'gyn-cervix.html': [
  ('105', 'Cervix definitive EBRT ± chemotherapy', p('gynaecological/105-gynaecological-cervix-definitive-ebrt-with-or')),
  ('1319', 'Cervix definitive brachytherapy boost', p('gynaecological/1319-gynaecological-cervix-definitive-brachytherap')),
  ('1471', 'Cervix adjuvant EBRT', p('gynaecological/1471-gynaecological-cervix-adjuvant-ebrt')),
  ('3026', 'Cervix adjuvant EBRT chemoradiation', p('gynaecological/3026-gynaecological-cervix-adjuvant-ebrt-chemoradi')),
 ],
 'gyn-endometrial.html': [
  ('233', 'Endometrium adjuvant EBRT ± chemotherapy', p('gynaecological/233-gynaecological-endometrium-adjuvant-ebrt-with')),
  ('3660', 'Endometrium adjuvant vaginal brachytherapy alone or boost', p('gynaecological/3660-gynaecological-endometrium-adjuvant-vaginal-b')),
  ('3746', 'Endometrium definitive EBRT ± chemotherapy', p('gynaecological/3746-gynaecological-endometrium-definitive-ebrt-wi')),
  ('3747', 'Endometrium definitive HDR brachytherapy alone or boost', p('gynaecological/3747-gynaecological-endometrium-definitive-hdr-bra')),
 ],
 'gyn-vulva-vagina.html': [
  ('3748', 'Vulval adjuvant EBRT post-operative', p('gynaecological/3748-gynaecological-vulval-adjuvant-ebrt-post-oper')),
  ('3749', 'Vulval definitive or neoadjuvant EBRT ± chemotherapy', p('gynaecological/3749-gynaecological-vulval-definitive-or-neoadjuva')),
  ('', 'All eviQ gynaecological radiation oncology protocols', CAT + 'Gynaecological'),
 ],
 'gyn-general.html': [
  ('', 'All eviQ gynaecological radiation oncology protocols', CAT + 'Gynaecological'),
 ],
}
