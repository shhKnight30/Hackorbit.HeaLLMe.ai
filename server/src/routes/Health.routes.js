import  Router  from "express";
import {
    createHealthReport,
    getHealthReportById,
    updateHealthReport,
    deleteHealthReport
} from "../controllers/health.controller.js";

const HealthRouter = Router();

HealthRouter.post("/create-health-report", createHealthReport);
HealthRouter.get("/:id", getHealthReportById);
HealthRouter.patch("/update-health-report/:id", updateHealthReport);
HealthRouter.delete("/delete-health-report/:id", deleteHealthReport);

export default HealthRouter;