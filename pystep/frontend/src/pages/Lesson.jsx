import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Editor from '@monaco-editor/react'
import { lessonsAPI, exercisesAPI, executeAPI } from '../services/api'
import { useAuthStore } from '../store/authStore'
import { 
  ArrowLeft, Play, Lightbulb, CheckCircle, XCircle, 
  AlertCircle, Loader, Trophy 
} from 'lucide-react'

export default function Lesson() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user, updateUser } = useAuthStore()

  const [lesson, setLesson] = useState(null)
  const [exercises, setExercises] = useState([])
  const [currentExercise, setCurrentExercise] = useState(0)
  const [code, setCode] = useState('# Escreva seu código aqui\n')
  const [output, setOutput] = useState('')
  const [feedback, setFeedback] = useState(null)
  const [loading, setLoading] = useState(false)
  const [executing, setExecuting] = useState(false)

  useEffect(() => {
    loadLesson()
  }, [id])

  const loadLesson = async () => {
    setLoading(true)
    try {
      const [lessonRes, exercisesRes] = await Promise.all([
        lessonsAPI.getById(id),
        exercisesAPI.getByLesson(id)
      ])
      
      setLesson(lessonRes.data)
      setExercises(exercisesRes.data)
      
      if (exercisesRes.data.length > 0) {
        setCode(exercisesRes.data[0].codigo_inicial)
      }
    } catch (error) {
      console.error('Erro ao carregar lição:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleRunCode = async () => {
    setExecuting(true)
    setFeedback(null)
    
    try {
      const response = await executeAPI.run({
        code,
        exercise_id: exercises[currentExercise].id,
        input_data: ''
      })
      
      const data = response.data
      setOutput(data.output || data.error)
      setFeedback(data.feedback)
      
      // Se passou, atualizar XP
      if (data.passed && data.xp_gained > 0) {
        updateUser({ xp: user.xp + data.xp_gained })
      }
      
    } catch (error) {
      setOutput('Erro ao executar código')
      console.error(error)
    } finally {
      setExecuting(false)
    }
  }

  const handleGetHint = async () => {
    try {
      const response = await executeAPI.getHint(exercises[currentExercise].id, code)
      setFeedback({
        feedback: response.data.hint,
        severity: 'info',
        encouragement: '💡 Dica revelada!'
      })
    } catch (error) {
      console.error('Erro ao buscar dica:', error)
    }
  }

  const handleNextExercise = () => {
    if (currentExercise < exercises.length - 1) {
      setCurrentExercise(currentExercise + 1)
      setCode(exercises[currentExercise + 1].codigo_inicial)
      setOutput('')
      setFeedback(null)
    } else {
      navigate('/dashboard')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-600 to-blue-600">
        <Loader className="w-12 h-12 text-white animate-spin" />
      </div>
    )
  }

  const exercise = exercises[currentExercise]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="p-2 hover:bg-gray-100 rounded-lg transition"
            >
              <ArrowLeft className="w-6 h-6" />
            </button>
            <div>
              <h1 className="text-xl font-bold text-gray-800">{lesson?.titulo}</h1>
              <p className="text-sm text-gray-900">
                Exercício {currentExercise + 1} de {exercises.length}
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 px-4 py-2 bg-yellow-50 rounded-lg">
              <Trophy className="w-5 h-5 text-yellow-600" />
              <span className="font-semibold text-yellow-700">{user.xp} XP</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto p-6">
        <div className="grid lg:grid-cols-2 gap-6">
          {/* Left: Descrição */}
          <div className="space-y-6">
            {/* Explicação da lição */}
            {lesson?.conteudo && (
              <div className="bg-white rounded-xl shadow p-6">
                <h2 className="text-lg font-bold text-gray-800 mb-4">📚 Teoria</h2>
                <div className="prose prose-sm" dangerouslySetInnerHTML={{ __html: lesson.conteudo }} />
              </div>
            )}

            {/* Exercício */}
            <div className="bg-white rounded-xl shadow p-6">
              <h2 className="text-lg font-bold text-gray-800 mb-4">🎯 Desafio</h2>
              <p className="text-gray-700 mb-4">{exercise?.descricao}</p>
              
              {exercise?.dica && (
                <button
                  onClick={handleGetHint}
                  className="flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium"
                >
                  <Lightbulb className="w-5 h-5" />
                  Ver dica
                </button>
              )}
            </div>

            {/* Console / Output */}
            <div className="bg-gray-900 rounded-xl shadow p-6 text-white">
              <h3 className="text-sm font-semibold mb-3 text-gray-800">Console</h3>
              <pre className="font-mono text-sm whitespace-pre-wrap">
                {output || 'Execute seu código para ver o resultado...'}
              </pre>
            </div>

            {/* Feedback da IA */}
            {feedback && (
              <div className={`rounded-xl shadow p-6 ${
                feedback.severity === 'success' ? 'bg-green-50 border-2 border-green-200' :
                feedback.severity === 'error' ? 'bg-red-50 border-2 border-red-200' :
                feedback.severity === 'warning' ? 'bg-yellow-50 border-2 border-yellow-200' :
                'bg-blue-50 border-2 border-blue-200'
              }`}>
                <div className="flex items-start gap-3">
                  {feedback.severity === 'success' && <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0" />}
                  {feedback.severity === 'error' && <XCircle className="w-6 h-6 text-red-600 flex-shrink-0" />}
                  {feedback.severity === 'warning' && <AlertCircle className="w-6 h-6 text-yellow-600 flex-shrink-0" />}
                  {feedback.severity === 'info' && <Lightbulb className="w-6 h-6 text-blue-600 flex-shrink-0" />}
                  
                  <div className="flex-1">
                    <p className="font-semibold mb-2">{feedback.feedback}</p>
                    {feedback.hint && <p className="text-sm mb-2">💡 {feedback.hint}</p>}
                    {feedback.encouragement && (
                      <p className="text-sm font-medium">{feedback.encouragement}</p>
                    )}
                    
                    {feedback.severity === 'success' && (
                      <button
                        onClick={handleNextExercise}
                        className="mt-4 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
                      >
                        {currentExercise < exercises.length - 1 ? 'Próximo Exercício' : 'Concluir Lição'}
                      </button>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Right: Editor */}
          <div className="space-y-4">
            <div className="bg-white rounded-xl shadow overflow-hidden">
              <div className="bg-gray-800 px-6 py-3 flex items-center justify-between">
                <span className="text-white font-semibold">editor.py</span>
                <button
                  onClick={handleRunCode}
                  disabled={executing}
                  className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition disabled:opacity-50"
                >
                  {executing ? (
                    <>
                      <Loader className="w-4 h-4 animate-spin" />
                      Executando...
                    </>
                  ) : (
                    <>
                      <Play className="w-4 h-4" />
                      Executar
                    </>
                  )}
                </button>
              </div>
              
              <Editor
                height="600px"
                defaultLanguage="python"
                theme="vs-dark"
                value={code}
                onChange={(value) => setCode(value || '')}
                options={{
                  fontSize: 14,
                  minimap: { enabled: false },
                  lineNumbers: 'on',
                  scrollBeyondLastLine: false,
                  automaticLayout: true,
                }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
