from aiogram import Router
from . import problem1_hand, problem2_hand, problem3_hand, problem4_hand

# Инициализация главного router для модуля 'problems'
router = Router()

# Включаем каждый обработчик проблемы в router
router.include_router(problem1_hand.router)
router.include_router(problem2_hand.router)
router.include_router(problem3_hand.router)
router.include_router(problem4_hand.router)
