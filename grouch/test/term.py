body = str("""
    <table class="dataentrytable" summary="This table is used for input criteria for catalog courses.">
<tbody><tr>
<td class="delabel" scope="row"><label for="subj_id"><span class="fieldlabeltext">Subject: </span></label></td>
<td class="dedefault">
<select name="sel_subj" size="3" multiple="" id="subj_id">
<option value="ACCT">Accounting
</option><option value="AE">Aerospace Engineering
</option><option value="AS">Air Force Aerospace Studies
</option><option value="APPH">Applied Physiology
</option><option value="ASE">Applied Systems Engineering
</option><option value="ARBC">Arabic
</option><option value="ARCH">Architecture
</option><option value="BIOL">Biology
</option><option value="BMEJ">Biomed Engr/Joint Emory PKU
</option><option value="BMED">Biomedical Engineering
</option><option value="BMEM">Biomedical Engr/Joint Emory
</option><option value="BC">Building Construction
</option><option value="CETL">Center Enhancement-Teach/Learn
</option><option value="CHBE">Chemical &amp; Biomolecular Engr
</option><option value="CHEM">Chemistry
</option><option value="CHIN">Chinese
</option><option value="CP">City Planning
</option><option value="CEE">Civil and Environmental Engr
</option><option value="COA">College of Architecture
</option><option value="COE">College of Engineering
</option><option value="COS">College of Sciences
</option><option value="CX">Computational Mod, Sim, &amp; Data
</option><option value="CSE">Computational Science &amp; Engr
</option><option value="CS">Computer Science
</option><option value="COOP">Cooperative Work Assignment
</option><option value="UCGA">Cross Enrollment
</option><option value="EAS">Earth and Atmospheric Sciences
</option><option value="ECON">Economics
</option><option value="ECEP">Elect &amp; Comp Engr-Professional
</option><option value="ECE">Electrical &amp; Computer Engr
</option><option value="ENGL">English
</option><option value="ENTR">Enterprise Transformation
</option><option value="FS">Foreign Studies
</option><option value="FREN">French
</option><option value="GT">Georgia Tech
</option><option value="GTL">Georgia Tech Lorraine
</option><option value="GRMN">German
</option><option value="HPS">Health Performance Science
</option><option value="HP">Health Physics
</option><option value="HS">Health Systems
</option><option value="HIN">Hindi
</option><option value="HIST">History
</option><option value="HTS">History, Technology &amp; Society
</option><option value="ISYE">Industrial &amp; Systems Engr
</option><option value="ID">Industrial Design
</option><option value="IPCO">Int'l Plan Co-op Abroad
</option><option value="IPIN">Int'l Plan Intern Abroad
</option><option value="IPFS">Int'l Plan-Exchange Program
</option><option value="IPSA">Int'l Plan-Study Abroad
</option><option value="INTA">International Affairs
</option><option value="IL">International Logistics
</option><option value="INTN">Internship
</option><option value="IMBA">Intl Executive MBA
</option><option value="IAC">Ivan Allen College
</option><option value="JAPN">Japanese
</option><option value="KOR">Korean
</option><option value="LATN">Latin
</option><option value="LS">Learning Support
</option><option value="LING">Linguistics
</option><option value="LCC">Lit, Communication &amp; Culture
</option><option value="LMC">Literature, Media &amp; Comm
</option><option value="MGT">Management
</option><option value="MOT">Management of Technology
</option><option value="MLDR">Manufacturing Leadership
</option><option value="MSE">Materials Science &amp; Engr
</option><option value="MATH">Mathematics
</option><option value="ME">Mechanical Engineering
</option><option value="MP">Medical Physics
</option><option value="MSL">Military Science &amp; Leadership
</option><option value="ML">Modern Languages
</option><option value="MUSI">Music
</option><option value="NS">Naval Science
</option><option value="NRE">Nuclear &amp; Radiological Engr
</option><option value="PERS">Persian
</option><option value="PHIL">Philosophy
</option><option value="PHYS">Physics
</option><option value="POL">Political Science
</option><option value="PTFE">Polymer, Textile and Fiber Eng
</option><option value="DOPP">Professional Practice
</option><option value="PSY">Psychology
</option><option value="PSYC">Psychology
</option><option value="PUBP">Public Policy
</option><option value="PUBJ">Public Policy/Joint GSU PhD
</option><option value="RUSS">Russian
</option><option value="SCI">Science
</option><option value="SOC">Sociology
</option><option value="SPAN">Spanish
</option></select>
</td>
</tr>
<tr>
<td class="delabel" scope="row"><label for="crse_id_from"><span class="fieldlabeltext">Course Number Range: </span></label></td>
<td colspan="7" class="dedefault"> from <input type="text" name="sel_crse_strt" size="6" maxlength="5" id="crse_id_from"><label for="crse_id_to"><span class="fieldlabeltextinvisible">Course To</span></label> to <input type="text" name="sel_crse_end" size="6" maxlength="5" id="crse_id_to"></td>
</tr>
<tr>
<td class="delabel" scope="row"><label for="title_id"><span class="fieldlabeltext">Title: </span></label></td>
<td colspan="7" class="dedefault"><input type="text" name="sel_title" size="33" maxlength="30" id="title_id"></td>
</tr>
<input type="hidden" name="sel_levl" value="%">
<input type="hidden" name="sel_schd" value="%">
<input type="hidden" name="sel_coll" value="%">
<input type="hidden" name="sel_divs" value="%">
<input type="hidden" name="sel_dept" value="%">
<tr>
<td class="delabel" scope="row"><label for="credit_id_from"><span class="fieldlabeltext">Credit Range: </span></label></td>
<td class="dedefault"><input type="text" name="sel_from_cred" size="11" maxlength="10" id="credit_id_from"> hours to <label for="credit_id_to"><span class="fieldlabeltextinvisible">Credit Range To:</span></label><input type="text" name="sel_to_cred" size="11" maxlength="10" id="credit_id_to"> hours
</td>
</tr>
<input type="hidden" name="sel_attr" value="%">
<tr>
<td class="dedefault"><input type="submit" value="Get Courses"></td>
<td class="dedefault"><input type="reset" value="Reset"></td>
</tr>
</tbody></table>
""")