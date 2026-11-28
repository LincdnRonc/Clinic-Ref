# Phone and contact list (Tools > Contacts). Edit this file, then run build.py; it writes src/contacts.html.
# Source: "Contact List - SVH" (Nov 2026).
# The repo is public: no mobile numbers and no staff names here. Those are in the CONTACTS_PRIVATE secret
# and added at deploy by tools/private_contacts.py (only onto the password-protected site). Use service names, extensions,
# landlines, faxes and shared mailboxes only.
# Numbers: a 4-5 digit number is shown as an internal extension; 8-digit Sydney numbers and 1300/1800 numbers
# become tap-to-call links. Separate several numbers with " / ".
# Each row: (service, number(s), note)

TABS = [
 ('gc-svh', 'GenesisCare SVH', "", [
  ('Level A (SVRO)', 'Main line 8302 5400', [
   ('Reception 1', '5401', ''),
   ('Reception 2', '5402', ''),
   ('Fax', '5410', ''),
   ('Accounts / interview', '5417', ''),
   ('Nursing station', '5416', ''),
   ('Consult 1 (nursing)', '5411', ''),
   ('Consult 2 (doctors)', '5414', ''),
   ('Planning', '5421 / 5426 / 5427 / 5428', ''),
   ('Sim', '5431', ''),
   ('SIMBA', '5430 / 5412 / 5422', ''),
  ]),
  ('Sacred Heart (SHRO)', 'Main line 8302 5450', [
   ('Reception', '5451 / 5452', 'Left / right'),
   ('Fax', '5460', ''),
   ('Consult room 1', '5462', ''),
   ('Consult room 2', '5465', ''),
   ('Consult room 3', '5464', ''),
   ('Consult room 4', '5463', ''),
   ('Consult room 5', '5461', ''),
   ('CL room', '5413', ''),
   ('Bookings', '8348 4455 / 5423', 'Main / direct extension'),
   ('Nurses', '5466 / 5419 / 5418', '5418 = back room'),
   ('Admin office (CNC room)', '5467', ''),
   ('Nala', '5480', ''),
   ('ACE', '5415', ''),
   ('Physics', '5471 / 5472 / 5473', ''),
   ('Planning', '5476 / 5477 / 5478', ''),
  ]),
  ('Level 7, Suite 708', '', [
   ('Reception', '5404 / 5403 / 5456', '5456 = back'),
   ('Consult 1 (left)', '5407', ''),
   ('Consult 2 (right)', '5406', ''),
   ('Fax', '5449', ''),
   ('Reception email', 'receptiononcologysvc@genesiscare.com', ''),
  ]),
  ('Other services', '', [
   ('PointGuard Connect', '02 8236 3311', ''),
   ('The Kinghorn Cancer Centre', '9355 5737', ''),
   ('Sacred Heart Hospice', '8382 9444', ''),
   ("St Vincent's Clinic Level 4 front desk", '8382 6222', ''),
   ('DVA Transport', '1800 550 455', 'Fax 9213 7171'),
   ("St Vincent's Private: financial services", '8382 4631', ''),
   ('GenesisCare IT', '1300 436 638', ''),
  ]),
 ]),
 ('svh', "St Vincent's Hospital", "", [
  ('Switch, paging and bookings', '', [
   ('Switch', '59', ''),
   ('Paging', '26888', 'Then pager number, then #'),
   ('Bookings', '8348 4455', ''),
   ('Bookings: direct line', '8348 4504', ''),
   ('CT sim', '8302 5427 / 8302 5426', ''),
   ('GenesisCare Level A', '5402', ''),
   ('GenesisCare Level 7', '5403', ''),
   ('Accommodation', '8382 2114', ''),
  ]),
  ('Services', '', [
   ('Pain / TPN', '6154', ''),
   ('Pathology', '29100', ''),
   ('Anatomical pathology', '29272', ''),
   ('Radiology registrar', '21860', ''),
   ('MRI', '21879 / 21878', 'Registrar? (as listed)'),
   ('Interventional radiology', '21896', ''),
   ('Ultrasound', '21884', ''),
   ('Dental', '23129', ''),
  ]),
  ('Plastics referral', '', [
   ('Email', 'svhs.gacreception@svha.org.au', ''),
   ('Fax', '8382 3111', ''),
  ]),
 ]),
 ('centres', 'GenesisCare centres', '', [
  # (centre, address, [(label, number)])
  ('Bella Vista (Norwest)', 'Level 3, Suite 311, 8 Elizabeth Macarthur Drive, Bella Vista NSW 2153', [('Phone', '02 8811 8400'), ('Email', 'norwest@genesiscare.com')]),
  ('Campbelltown', '38 Camden Rd, Campbelltown NSW 2560', [('Phone', '02 4632 5500'), ('Email', 'admin.campbelltown@genesiscare.com')]),
  ('Frenchs Forest', 'Suite 3, Level 1, Building 1, 49 Frenchs Forest Rd, Frenchs Forest East NSW 2086', [('Phone', '9470 5300')]),
  ('GenesisCare head office', 'Building 1, The Mill, 2 Huntley St, Alexandria NSW 2015', [('Phone', '02 8236 3300'), ('IT help desk', '1300 436 638'), ('Payroll', '02 8236 3330')]),
  ('Kingswood', 'Somerset Private Hospital, Kingswood NSW 2747', [('Phone', '4726 8700')]),
  ('Macquarie University Hospital', 'Suite 1, Basement Level 2, 3 Technology Place, Macquarie University NSW 2109', [('Phone', '02 9812 3220'), ('Fax', '02 9812 3389')]),
  ('Maitland', '30 Metford Rd, East Maitland NSW 2323', [('Phone', '4918 4500')]),
  ('Mater Private Hospital', '25 Rocklands Road, Crows Nest NSW 2065', [('Phone', '02 9458 8050'), ('Fax', '02 9929 2687')]),
  ('Newcastle (Lake Macquarie Private Hospital)', '36 Pacific Highway, Gateshead NSW 2290', [('Phone', '02 4918 4500 / 02 4918 4501 / 02 4918 4502')]),
  ('North Shore Health Hub', 'Tower A, Level 1, 7 Westbourne St, St Leonards NSW 2065', [('Phone', '8037 4100'), ('Fax', '8037 4111')]),
  ('Waratah Private Hospital (Hurstville)', '31 Dora Street, Hurstville NSW 2220', [('Phone', '02 8568 7600')]),
 ]),
]

# Shown on the page so it is clear what was left off (no numbers or names).
NOT_HERE = ('Mobile numbers and staff names are added only to the password-protected site when it deploys, '
            'so they are missing from this copy. Use the printed SVH contact list.')
