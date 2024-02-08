from . import problem1_hand, problem2_hand, problem3_hand, problem4_hand
from aiogram import Router

# Initialize the main router for the 'problems' module
router = Router()

# Include each problem handler router
router.include_router(problem1_hand.router)
router.include_router(problem2_hand.router)
router.include_router(problem3_hand.router)
router.include_router(problem4_hand.router)