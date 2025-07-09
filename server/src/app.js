import express from "express"
import cors from "cors"


const app = express()

app.use(cors())

app.use(express.json({
    limit: '3mb'
}));

app.use(express.urlencoded({
    extended: true,
    limit: '10mb'
}));

app.use(express.static('public'));

import Sessionrouter from "./routes/sessions.routes.js";
import SymptomsRouter from "./routes/Symptoms.routes.js";
import MessageRouter from "./routes/Message.route.js";
import HealthRouter from "./routes/Health.routes.js";

app.use("/api/v1/sessions", Sessionrouter);
app.use("/api/v1/symptoms", SymptomsRouter);   
app.use("/api/v1/messages", MessageRouter);
app.use("/api/v1/health", HealthRouter);


export { app }