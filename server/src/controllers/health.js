import asynchandler from "../utils/asynchandler.js";
import ApiError from "../utils/ApiError.js";
import ApiResponse from "../utils/apiresponse.js"; 
import Symptoms from "../models/Symptoms.js";

const createHealthReport = asynchandler(async (req, res) => {
    const { reports, symptoms, medications } = req.body;

    if (!reports || !symptoms || !medications) {
        throw new ApiError(400, "All fields are required");
    }

    const newHealthReport = await Symptoms.create({
        reports,
        symptoms,
        medications
    });

    res.status(201).json(new ApiResponse(200, "Health report created successfully", newHealthReport));
})

const getHealthReportById = asynchandler(async (req, res) => {
    const { id } = req.params;
    const healthReport = await Symptoms.findById(id).populate('symptoms');

    if (!healthReport) {
        throw new ApiError(404, "Health report not found");
    }
    res.status(200).json(new ApiResponse(200, "Health report retrieved successfully", healthReport));
})

const updateHealthReport = asynchandler(async (req, res) => {
    const { id } = req.params;
    const { reports, symptoms, medications } = req.body;

    if (!reports || !symptoms || !medications) {
        throw new ApiError(400, "All fields are required");
    }

    const updatedHealthReport = await Symptoms.findByIdAndUpdate(id, {
        reports,
        symptoms,
        medications
    }, { new: true });

    if (!updatedHealthReport) {
        throw new ApiError(404, "Health report not found");
    }

    res.status(200).json(new ApiResponse(200, "Health report updated successfully", updatedHealthReport));
})

const deleteHealthReport = asynchandler(async (req, res) => {
    const { id } = req.params;
    const deletedHealthReport = await Symptoms.findByIdAndDelete(id);

    if (!deletedHealthReport) {
        throw new ApiError(404, "Health report not found");
    }

    res.status(200).json(new ApiResponse(200, "Health report deleted successfully", deletedHealthReport));
})

export {
    createHealthReport,
    getHealthReportById,
    updateHealthReport,
    deleteHealthReport
};
