const fs=require("fs"),path=require("path"),vm=require("vm");
const src=process.argv[2];
const gens=fs.readdirSync(src).filter(f=>/^data_gen\d+\.js$/.test(f)).sort((a,b)=>+a.match(/\d+/)[0]-+b.match(/\d+/)[0]);
const code=["data_core.js",...gens,"i18n.js","stats.js"].map(f=>fs.readFileSync(path.join(src,f),"utf8")).join("\n")+"\n;({P,K})";
const {P,K}=vm.runInNewContext(code,{console});
console.log(JSON.stringify({P,K}));
