import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { lessonsAPI } from '../services/api'
import { Code2, Trophy, Star, BookOpen, LogOut, CheckCircle, Lock as LockIcon } from 'lucide-react'

export default function Dashboard() {
  const { user, logout } = useAuthStore()
  const [lessons, setLessons] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (user && user.id) {
      loadLessons()
    }
  }, [user])

  const loadLessons = async () => {
    try {
      const response = await lessonsAPI.getAll()
      // Adicionar lógica de desbloqueio baseada no nível do usuário
      const lessonsWithLock = response.data.map(lesson => ({
        ...lesson,
        is_unlocked: lesson.nivel <= user.nivel_atual,
        is_completed: false // TODO: implementar quando tiver backend de progresso
      }))
      setLessons(lessonsWithLock)
    } catch (error) {
      console.error('Erro ao carregar lições:', error)
    } finally {
      setLoading(false)
    }
  }

  const levelProgress = ((user.xp % 100) / 100) * 100

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-blue-600 p-6">
      {/* Header */}
      <header className="max-w-6xl mx-auto mb-8">
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 text-white">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Code2 className="w-10 h-10" />
              <div>
                <h1 className="text-2xl font-bold">Olá, {user.nome}! 👋</h1>
                <p className="text-white">Continue sua jornada Python</p>
              </div>
            </div>
            <button
              onClick={logout}
              className="flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg transition"
            >
              <LogOut className="w-4 h-4" />
              Sair
            </button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4 mt-6">
            <div className="bg-white/10 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <Trophy className="w-5 h-5 text-yellow-300" />
                <span className="text-sm">XP Total</span>
              </div>
              <p className="text-3xl font-bold">{user.xp}</p>
            </div>

            <div className="bg-white/10 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <Star className="w-5 h-5 text-blue-300" />
                <span className="text-sm">Nível</span>
              </div>
              <p className="text-3xl font-bold">{user.nivel_atual}</p>
            </div>

            <div className="bg-white/10 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <BookOpen className="w-5 h-5 text-green-300" />
                <span className="text-sm">Lições</span>
              </div>
              <p className="text-3xl font-bold">{lessons.length}</p>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="mt-6">
            <div className="flex justify-between text-sm mb-2">
              <span>Progresso para Nível {user.nivel_atual + 1}</span>
              <span>{user.xp % 100}/100 XP</span>
            </div>
            <div className="bg-white/20 rounded-full h-3 overflow-hidden">
              <div
                className="bg-gradient-to-r from-green-400 to-blue-400 h-full transition-all duration-500"
                style={{ width: `${levelProgress}%` }}
              />
            </div>
          </div>
        </div>
      </header>

      {/* Lessons Grid */}
      <main className="max-w-6xl mx-auto">
        <h2 className="text-2xl font-bold text-white mb-6">Suas Lições</h2>

        {loading ? (
          <div className="text-white text-center">Carregando lições...</div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {lessons.map((lesson, idx) => (
              <div
                key={lesson.id}
                className={`bg-white rounded-xl shadow-lg p-6 hover:shadow-2xl transition-all animate-slide-in ${!lesson.is_unlocked ? 'opacity-50 pointer-events-none' : 'hover:scale-105'}`}
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <span className="inline-block px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm font-semibold mb-2">
                      Nível {lesson.nivel}
                    </span>
                    <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
                      {lesson.titulo}
                      {lesson.is_completed && <CheckCircle className="w-5 h-5 text-green-500" title="Concluída" />}
                    </h3>
                  </div>
                  <BookOpen className="w-8 h-8 text-primary-500" />
                </div>
                <p className="text-gray-800 mb-4 line-clamp-2">{lesson.descricao}</p>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-900">{lesson.xp_total} XP</span>
                  {lesson.is_unlocked ? (
                    <Link to={`/lesson/${lesson.id}`} className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition">
                      {lesson.is_completed ? 'Rever' : 'Começar'}
                    </Link>
                  ) : (
                    <button className="px-4 py-2 bg-gray-300 text-gray-500 rounded-lg flex items-center gap-2 cursor-not-allowed" disabled>
                      <LockIcon className="w-4 h-4" /> Bloqueada
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {!loading && lessons.length === 0 && (
          <div className="text-center text-white bg-white/10 backdrop-blur rounded-xl p-12">
            <BookOpen className="w-16 h-16 mx-auto mb-4 opacity-50" />
            <p className="text-xl">Nenhuma lição disponível ainda.</p>
            <p className="text-white mt-2">Em breve novas lições serão adicionadas!</p>
          </div>
        )}
      </main>
    </div>
  )
}
