body = str("""
<div class="pagebodydiv">
<!--  ** END OF twbkwbis.P_OpenDoc **  -->
<div class="infotextdiv"><table class="infotexttable" summary="This layout table contains information that may be helpful in understanding the content and functionality of this page.  It could be a brief set of instructions, a description of error messages, or other special information."><tbody><tr><td class="indefault"><img src="/wtlgifs/web_info_cascade.png" alt="Information" class="headerImg" title="Information" name="web_info" hspace="0" vspace="0" border="0" height="12" width="14"></td><td class="indefault"><span class="infotext"> Please select a Catalog term and choose Submit to proceed to the Course Search page.</span></td></tr></tbody></table><p></p></div>
<form action="/pls/bprod/bwckctlg.p_disp_cat_term_date" method="post">
<input type="hidden" name="call_proc_in" value="bwckctlg.p_disp_dyn_ctlg">
<table class="dataentrytable" summary="This layout table is used for catalog term for the dynamic catalog." width="100%"><caption class="captiontext">Search by Term: </caption>
<tbody><tr>
<td class="dedefault"><label for="term_input_id"><span class="fieldlabeltextinvisible">Term</span></label>
<select name="cat_term_in" size="1" id="term_input_id">
<option value="None">None
</option><option value="201602">Spring 2016
</option><option value="201528">Language Inst IEP Fall 2 2015
</option><option value="201527">Language Inst IEP Fall 1 2015
</option><option value="201508">Fall 2015
</option><option value="201505">Summer 2015
</option><option value="201502">Spring 2015
</option><option value="201408">Fall 2014
</option><option value="201405">Summer 2014
</option><option value="201402">Spring 2014
</option><option value="201328">Language Institute Fall 2 2013
</option><option value="201327">Language Institute Fall 1 2013
</option><option value="201326">Language Institute Fall 2013
</option><option value="201325">Lang Inst Summer Spc Prog 2013
</option><option value="201324">Lang Inst Summer IEP 2013
</option><option value="201323">Language Institute May 2013
</option><option value="201321">Language Institute Spring 1 13
</option><option value="201308">Fall 2013
</option><option value="201305">Summer 2013
</option><option value="201302">Spring 2013
</option><option value="201228">Language Institute Fall 2 2012
</option><option value="201227">Language Institute Fall 1 2012
</option><option value="201225">Lang Inst Summer Spc Prog 2012
</option><option value="201224">Lang Institute Summer IEP 2012
</option><option value="201222">Language Institute Spring 2 12
</option><option value="201221">Language Institute Spring 1 12
</option><option value="201208">Fall 2012
</option><option value="201205">Summer 2012
</option><option value="201202">Spring 2012
</option><option value="201128">Language Institute Fall 2 11
</option><option value="201127">Language Institute Fall 1 11
</option><option value="201125">Lang Inst Summer Spc Prog 2011
</option><option value="201124">Lang Institute Summer IEP 2011
</option><option value="201123">Language Institute May 2011
</option><option value="201122">Language Institute Spring 2 11
</option><option value="201121">Language Institute Spring 1 11
</option><option value="201108">Fall 2011
</option><option value="201105">Summer 2011
</option><option value="201102">Spring 2011
</option><option value="201028">Language Institute Fall 2 2010
</option><option value="201027">Language Institute Fall 1 2010
</option><option value="201025">Language Institute July 2010
</option><option value="201024">Language Institute Summer 2010
</option><option value="201023">Language Institute May 2010
</option><option value="201022">Language Institute Spring 2 10
</option><option value="201021">Language Institute Spring 1 10
</option><option value="201008">Fall 2010
</option><option value="201005">Summer 2010
</option><option value="201002">Spring 2010
</option><option value="200928">Language Institute Fall 2 2009
</option><option value="200927">Language Institute Fall 1 2009
</option><option value="200926">Language Institute August 2009
</option><option value="200925">Language Institute July 2009
</option><option value="200924">Language Institute Summer 09
</option><option value="200923">Language Institute May 2009
</option><option value="200922">Language Institute Spring 2 09
</option><option value="200921">Language Institute Spring 1 09
</option><option value="200908">Fall 2009
</option><option value="200905">Summer 2009
</option><option value="200902">Spring 2009
</option><option value="200828">Language Institute Fall 2 2008
</option><option value="200827">Language Institute Fall 1 2008
</option><option value="200824">Language Institute Summer 2008
</option><option value="200822">Language Institute Spring 2 08
</option><option value="200821">Language Institute Spring 1 08
</option><option value="200808">Fall 2008
</option><option value="200805">Summer 2008
</option><option value="200802">Spring 2008
</option><option value="200722">Language Institute Spring 2 07
</option><option value="200721">Language Institute Spring 1 07
</option><option value="200708">Fall 2007
</option><option value="200705">Summer 2007
</option><option value="200702">Spring 2007
</option><option value="200625">Language Institute Fall 2 2006
</option><option value="200608">Fall 2006
</option><option value="200605">Summer 2006
</option><option value="200602">Spring 2006
</option><option value="200508">Fall 2005
</option><option value="200505">Summer 2005
</option><option value="200502">Spring 2005
</option><option value="200408">Fall 2004
</option><option value="200405">Summer 2004
</option><option value="200402">Spring 2004
</option><option value="200308">Fall 2003
</option><option value="200305">Summer 2003
</option><option value="200302">Spring 2003
</option><option value="200208">Fall 2002
</option><option value="200205">Summer 2002
</option><option value="200202">Spring 2002
</option><option value="200108">Fall 2001
</option><option value="200105">Summer 2001
</option><option value="200102">Spring 2001
</option><option value="200008">Fall 2000
</option><option value="200005">Summer 2000
</option><option value="200002">Spring 2000
</option><option value="199908">Fall 1999
</option><option value="199906">Summer 1999
</option><option value="199903">Spring 1999
</option><option value="199901">Winter 1999
</option><option value="199809">Fall 1998
</option><option value="199806">Summer 1998
</option><option value="199803">Spring 1998
</option><option value="199801">Winter 1998
</option><option value="199709">Fall 1997
</option><option value="199706">Summer 1997
</option><option value="199703">Spring 1997
</option><option value="199701">Winter 1997
</option><option value="199609">Fall 1996
</option><option value="199606">Summer 1996
</option></select>
</td>
</tr>
</tbody></table>
<br>
<br>
<input type="submit" value="Submit">
</form>

<!--  ** START OF twbkwbis.P_CloseDoc **  -->
<table class="plaintable" summary="This is table displays line separator at end of the page." width="100%" cellspacing="0" cellpadding="0" border="0"><tbody><tr><td class="bgtabon" width="100%" colspan="2"><img src="/wtlgifs/web_transparent.gif" alt="Transparent Image" class="headerImg" title="Transparent Image" name="web_transparent" hspace="0" vspace="0" border="0" height="3" width="10"></td></tr></tbody></table>
<a href="#top" onmouseover="window.status='Skip to top of page'; return true" onmouseout="window.status=''; return true" onfocus="window.status='Skip to top of page'; return true" onblur="window.status=''; return true" class="skiplinks">Skip to top of page</a>
</div>
""")