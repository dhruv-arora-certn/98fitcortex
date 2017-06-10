pdf_style =     '''@page {
        size: Letter;
        margin: 0in 0.44in 0.2in 0.44in;
    }
    body, div, p {
      font-family: 'Calibri';
      font-size: 11px;
    }
  
    .gradient {
      border:0.1mm solid #220044; 
      background-color: #f0f2ff;
      background-gradient: linear #c7cdde #f0f2ff 0 1 0 0.5;
      box-shadow: 0.3em 0.3em #888888;
    }
    h4 {
      font-weight: bold;
      margin-top: 1em;
      margin-bottom: 0.3em;
      margin-top: 0;
    }
    div.text {
      padding:0.8em; 
      margin-bottom: 0.7em;
    }
    p { margin: 0.25em 0; }
    p.code {
      background-color: #e5e5e5; 
      margin: 1em 1cm;
      padding: 0 0.3cm;
      border:0.2mm solid #000088; 
      box-shadow: 0.3em 0.3em #888888;
    }
    p.example, div.example {
      background-color: #eeeeee; 
      margin: 0.3em 1em 1em 1em;
      padding: 0 0.3cm;
      border:0.2mm solid #444444; 
    }
    .code {
      font-family: monospace;
      font-size: 9pt;
    }
    .shadowtitle { 
      height: 8mm; 
      background-color: #EEDDFF; 
      background-gradient: linear #c7cdde #f0f2ff 0 1 0 0.5;  
      padding: 0.8em; 
      padding-left: 3em;
      font-family:sans;
      font-size: 26pt; 
      font-weight: bold;
      border: 0.2mm solid white;
      border-radius: 0.2em;
      box-shadow: 0 0 1em 0.5em rgba(0,0,255,0.5);
      color: #AAAACC;
      text-shadow: 0.03em 0.03em #666, 0.05em 0.05em rgba(127,127,127,0.5), -0.015em -0.015em white;
    }
    h3 { 
      margin: 3em 0 2em -15mm; 
      background-color: #EEDDFF; 
      background-gradient: linear #c7cdde #f0f2ff 0 1 0 0.5;  
      padding: 0.5em; 
      padding-left: 3em;
      width: 50%;
      font-family:sans;
      font-size: 16pt; 
      font-weight: bold;
      border-left: none;
      border-radius: 0 2em 2em 0;
      box-shadow: 0 0 2em 0.5em rgba(255,0,0,1);
      text-shadow: 0.05em 0.04em rgba(127,127,127,0.5);
    }
    .css {
      font-family: arial;
      font-style: italic;
      color: #000088;
    }
    img.smooth {
      image-rendering:auto;
      image-rendering:optimizeQuality;
      -ms-interpolation-mode:bicubic;
    }
    img.crisp {
      image-rendering: -moz-crisp-edges;    /* Firefox */
      image-rendering: -o-crisp-edges;    /* Opera */
      image-rendering: -webkit-optimize-contrast;/* Webkit (non-standard naming) */
      image-rendering: crisp-edges;
      -ms-interpolation-mode: nearest-neighbor; /* IE (non-standard property) */
    }
    .dotborder{
      border-bottom: solid 1px #0f80e5;
    }
    .alignleft{
      text-align: left;
    }
    .aligncenter{
      text-align: center;
    }
    .list {
            list-style-type: circle !important;
            list-style:circle !important;
            
        }'''