import  Router  from "express";
import {
    createSymptom,
    getSymptomById,
    updateSymptom,
    deleteSymptom
} from "../controllers/Symptoms.controller.js";

const SymptomsRouter = Router();

SymptomsRouter.post("/create-symptom", createSymptom);
SymptomsRouter.get("/:id", getSymptomById);
SymptomsRouter.patch("/update-symptom/:id", updateSymptom);
SymptomsRouter.delete("/delete-symptom/:id", deleteSymptom);

export default SymptomsRouter;