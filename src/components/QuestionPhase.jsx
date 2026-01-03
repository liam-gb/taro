import Button from './Button'

export default function QuestionPhase({ question, onQuestionChange, onContinue }) {
  return (
    <div className="max-w-md mx-auto text-center">
      <p className="text-slate-500 mb-6">What guidance do you seek?</p>
      <textarea
        value={question}
        onChange={(e) => onQuestionChange(e.target.value)}
        placeholder="Your question (or leave blank)..."
        className="w-full bg-slate-900/50 border border-slate-700 rounded-lg p-4 text-slate-200
          placeholder-slate-600 focus:outline-none focus:border-violet-500/50 resize-none mb-6"
        rows={3}
      />
      <Button onClick={onContinue} variant="secondary" fullWidth>
        Continue
      </Button>
    </div>
  )
}
