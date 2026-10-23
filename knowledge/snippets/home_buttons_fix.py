import subprocess, sys
NL = chr(10)
args = ["python", "patch_live.py", "--post-id", "276", "--page"]
for card in ["<!-- CARD 1: CRM OPERATIONS -->", "<!-- CARD 2: CLIENT ONBOARDING -->"]:
    old = card + NL + '    <div style="background: #ffffff;'
    args += ["--replace", old, card + NL + '    <div style="display: flex; flex-direction: column; background: #ffffff;']
for h3 in ["CRM &amp; Client Operations", "Client Onboarding &amp; Workflows"]:
    old = '<div style="padding: 24px; text-align: center;">' + NL + '        <h3 style="font-size: 22px; font-weight: 700; color: #0f172a; margin: 0 0 10px 0;">' + h3
    args += ["--replace", old, old.replace('padding: 24px; text-align: center;', 'flex: 1; display: flex; flex-direction: column; padding: 24px; text-align: center;')]
for href in ["what-is-client-relationship-management-software/", "client-onboarding-software/"]:
    old = '<a href="' + href + '" style="display: inline-block; width: 100%;'
    args += ["--replace", old, '<a href="' + href + '" style="margin-top: auto; display: inline-block; width: 100%;']
sys.exit(subprocess.run(args + sys.argv[1:]).returncode)
