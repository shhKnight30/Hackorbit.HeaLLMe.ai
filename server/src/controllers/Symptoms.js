import asynchandler from "../utils/asynchandler.js";
import ApiError from "../utils/ApiError.js";
import ApiResponse from "../utils/apiresponse.js"; 
import Symptoms from "../models/Symptoms.js";

createSymptom = asynchandler(async (req,res) => {
    const { symptom, severity, duration } = req.body;

    if (!symptom || !severity || !duration) {
        throw new ApiError(400, "All fields are required");
    }

    const newSymptom = await Symptoms.create({
        symptom,
        severity,
        duration
    });

    res.status(201).json(new ApiResponse(200,"Symptom created successfully", newSymptom));
})


getSymptomById = asynchandler(async (req, res) => {
    const {id} = req.params;
    const symptom = await Symptoms.findById(id);

    if(!symptom) {
        throw new ApiError(404, "Symptom not found");
    }
    res.status(200).json(new ApiResponse(200, "Symptom retrieved successfully", symptom));
})

updateSymptom = asynchandler(async (req, res) => {
    const {id} = req.params;
    const { symptom, severity, duration } = req.body;

    if (!symptom || !severity || !duration) {
        throw new ApiError(400, "All fields are required");
    }

    const updatedSymptom = await Symptoms.findByIdAndUpdate(id, {
        symptom,
        severity,
        duration
    }, { new: true });

    if (!updatedSymptom) {
        throw new ApiError(404, "Symptom not found");
    }

    res.status(200).json(new ApiResponse(200,"Symptom updated successfully", updatedSymptom));
})

deleteSymptom = asynchandler(async (req, res) => {
    const {id} = req.params;
    const deletedSymptom = await Symptoms.findByIdAndDelete(id);

    if (!deletedSymptom) {
        throw new ApiError(404, "Symptom not found");
    }

    res.status(200).json(new ApiResponse(200,"Symptom deleted successfully", deletedSymptom));
})

export {
    createSymptom,
    getSymptomById,
    updateSymptom,
    deleteSymptom
}