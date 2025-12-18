import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { ArrowLeft, User, Mail, Trophy, Star } from 'lucide-react'

export default function Profile() {
  const navigate = useNavigate()
  const { user } = useAuthStore()

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-blue-600 p-6">
      <div className="max-w-4xl mx-auto">
        <button
          onClick={() => navigate('/dashboard')}
          className="flex items-center gap-2 text-white mb-6 hover:underline"
        >
          <ArrowLeft className="w-5 h-5" />
          Voltar ao Dashboard
        </button>

        <div className="bg-white rounded-2xl shadow-2xl p-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-8">Meu Perfil</h1>

          <div className="space-y-6">
            {/* Info pessoal */}
            <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
              <User className="w-8 h-8 text-primary-600" />
              <div>
                <p className="text-sm text-gray-900">Nome</p>
                <p className="font-semibold text-gray-800">{user.nome}</p>
              </div>
            </div>

            <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
              <Mail className="w-8 h-8 text-primary-600" />
              <div>
                <p className="text-sm text-gray-900">Email</p>
                <p className="font-semibold text-gray-800">{user.email}</p>
              </div>
            </div>

            {/* Stats */}
            <div className="grid md:grid-cols-2 gap-4 mt-8">
              <div className="flex items-center gap-4 p-6 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-xl text-white">
                <Trophy className="w-12 h-12" />
                <div>
                  <p className="text-sm opacity-90">XP Total</p>
                  <p className="text-3xl font-bold">{user.xp}</p>
                </div>
              </div>

              <div className="flex items-center gap-4 p-6 bg-gradient-to-br from-blue-400 to-purple-500 rounded-xl text-white">
                <Star className="w-12 h-12" />
                <div>
                  <p className="text-sm opacity-90">Nível</p>
                  <p className="text-3xl font-bold">{user.nivel_atual}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
