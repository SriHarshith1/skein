import { connect } from "../src/lib/db";
import { migrate } from "../src/lib/migrate";

const sql = connect();
const applied = await migrate(sql);
console.log(applied.length ? `applied: ${applied.join(", ")}` : "schema up to date");
await sql.end();
