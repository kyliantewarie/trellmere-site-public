<h2>Stop round-tripping your sheet-metal parts through a second CAD program.</h2>
<p>SheetFab is a Blender extension that turns a folded sheet-metal part into a manufacturing-ready flat pattern — with the bend math done properly, inside the app you already model in.</p>
<figure><img src="{{SHOT1}}"><p class="figcaption">A folded box becomes a flat blank with bend lines — all inside Blender.</p></figure>

<h3>What it does</h3>
<ul>
<li><strong>Build parts in the panel.</strong> Material preset, thickness, inside radius, K-factor, leg lengths, bend angles, widths and holes. No JSON required — but power users can still use it.</li>
<li><strong>Real bend math.</strong> Bend allowance, bend deduction and outside-setback calculated from thickness, inside radius and K-factor — not a visual approximation.</li>
<li><strong>See the flat blank.</strong> Cut outline, bend lines with UP/DOWN direction, and hole circles in one preview.</li>
<li><strong>Export clean manufacturing files.</strong> Layered DXF (CUT, BEND_UP, BEND_DOWN, HOLES, INFO), a CSV bend table you can check against your shop, and an SVG preview.</li>
<li><strong>Nest and compensate kerf.</strong> Shape-aware nesting places copies on a sheet; kerf compensation offsets the cut path by half your tool diameter.</li>
<li><strong>Import 2D STEP geometry.</strong> POLYLINE, LINE, B_SPLINE control polygons and CIRCLEs from AP203/AP214 text files.</li>
</ul>
<figure><img src="{{SHOT2}}"><p class="figcaption">Nesting keeps bend lines and part spacing intact.</p></figure>

<h3>Who it's for</h3>
<p>Sheet-metal fabricators, product designers and makers who model in Blender and currently export to another CAD tool just to get a flat pattern for the laser or press brake.</p>

<h3>What it is not</h3>
<ul>
<li>Not a general CAD package.</li>
<li>Not a CAM toolpath generator — your cutting software still owns laser settings and toolpaths.</li>
<li>Not a substitute for calibrating your own K-factor. <strong>Bend a test coupon and measure it before production.</strong></li>
</ul>

<h3>What you get</h3>
<ul>
<li>The Blender 4.2+ extension (install from disk)</li>
<li>Full source under GPL-3.0-or-later</li>
<li>Free updates for the 1.x line</li>
<li>Direct support from the person who wrote it</li>
</ul>
<figure><img src="{{SHOT3}}"><p class="figcaption">A layered DXF — cut geometry and bend data in one export.</p></figure>

<h3>Compatibility &amp; confidence</h3>
<p>Tested on Windows with Blender 4.2.23 LTS and 5.3.0. The code is platform-independent; macOS and Linux are untested.</p>
<p><strong>Verified, not claimed:</strong> 236 automated checks, 43 artifact checks, a strict DXF audit and real smoke tests on two Blender versions.</p>
<p>Everything runs locally. No cloud, no telemetry, no licence server, no subscription.</p>
