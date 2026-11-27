<h2>Your AI-generated model looks great. It will not fit on your printer.</h2>
<p>SplitForge is a Blender extension that turns an oversized, fused mesh into a set of printable parts in one panel. No cloud, no licence server, no round-trip through another tool.</p>
<figure><img src="{{SHOT1}}"><p class="figcaption">One fused shell becomes separate, capped parts.</p></figure>

<h3>How it works</h3>
<ol>
<li><strong>Analyse</strong> the model against your build volume (X/Y/Z plus clearance).</li>
<li><strong>Plan shape-aware cuts.</strong> The planner looks for planes that cross the least geometry — a narrow neck — instead of blindly bisecting the bounding box.</li>
<li><strong>Split</strong> into capped, watertight parts that each fit the printer. The original mesh is untouched.</li>
<li><strong>Join them back</strong> with fitted pegs and sockets, dowel holes or magnet pockets.</li>
<li><strong>Hollow</strong> each part with a real millimetre wall and drill a drain hole at the lowest point.</li>
<li><strong>Check the fit</strong> with an exploded view, lay every part flat, and export one STL per part.</li>
</ol>
<figure><img src="{{SHOT2}}"><p class="figcaption">Editable curved seams and fitted connectors.</p></figure>

<h3>Made for</h3>
<p>Miniatures, busts, cosplay props, terrain, scans and meshes from Meshy / Tripo / Rodin / Hunyuan3D.</p>

<h3>What you get</h3>
<ul>
<li>The Blender 4.2–5.3 extension (zip, install from disk)</li>
<li>Full Python source under GPL-3.0-or-later</li>
<li>Pure-Python planning core (30 unit tests) plus a headless Blender smoke test</li>
<li>A sample .blend and a demo GIF</li>
<li>Free updates for the 1.x line</li>
</ul>

<h3>Honest limitations</h3>
<ul>
<li>Cut smoothness depends on mesh density — a coarse mesh gives a stair-stepped edge.</li>
<li>Connectors attach to flat cut faces; very thin or curved faces can be skipped. Check the <strong>Verify Assembly</strong> report before export.</li>
<li>Hollowing needs a watertight part; the Analyse step warns you if the mesh is not watertight.</li>
<li>STL export only — no 3MF plate packing, slicer integration or automatic supports.</li>
<li>Material presets give starting clearances, not a calibrated profile for your printer. Print a test coupon first.</li>
</ul>
<figure><img src="{{SHOT3}}"><p class="figcaption">Verify Assembly checks connector alignment before you export.</p></figure>

<h3>Verified</h3>
<p>Deterministic planning: the same mesh and settings always produce the same cuts. A 20,000-vertex mesh plans in about 0.06 s. The full verification suite is included in the download.</p>
<p>All sales final on the marketplace — but if the add-on cannot cut your model, message me before giving up and I will help you sort it out.</p>
