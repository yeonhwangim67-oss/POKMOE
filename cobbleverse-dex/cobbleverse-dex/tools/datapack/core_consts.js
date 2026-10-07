const fs=require("fs"),vm=require("vm");
const code=fs.readFileSync(process.argv[2],"utf8");
const names=[...code.matchAll(/(?:const|,)\s*([A-Z][A-Z0-9_]*)\s*=\s*\[/g)].map(m=>m[1]);
const ctx=vm.runInNewContext(code+"\n;({"+names.join(",")+"})",{console});
console.log(JSON.stringify(ctx));
