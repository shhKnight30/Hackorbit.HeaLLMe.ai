import  Router  from "express";
import {
    createMessage,
    getMessageById,
    updateMessage,
    deleteMessage
} from "../controllers/message.controller.js";

const MessageRouter = Router();

MessageRouter.post("/create-message", createMessage);
MessageRouter.get("/:id", getMessageById);
MessageRouter.patch("/update-message/:id", updateMessage);
MessageRouter.delete("/delete-message/:id", deleteMessage);

export default MessageRouter;