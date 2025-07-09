import Router from 'express';
import { getSessionById , createSession, deleteSession } from '../controllers/sessions.controller.js';

const Sessionrouter = Router();

Sessionrouter.get('/:id', getSessionById);
Sessionrouter.post('/create-session', createSession);
Sessionrouter.delete('/delete-session/:id', deleteSession);

export default Sessionrouter;