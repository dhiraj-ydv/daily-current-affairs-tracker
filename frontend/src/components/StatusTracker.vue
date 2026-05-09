<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import axios from 'axios'
import { format, isSameWeek, isSameMonth, isSameYear, parseISO } from 'date-fns'
import { Trash2, Edit2, Plus, Calendar, BookOpen, Layers, MessageSquare, PlusCircle } from 'lucide-vue-next'

const API_URL = 'http://localhost:8001'
const AVAILABLE_SOURCES = ['The Hindu', 'Indian Express', 'PIB', 'Monthly Magazine']
const STATUS_OPTIONS = ['Read', 'Partial', 'Not Read']

const statuses = ref([])
const today = format(new Date(), 'yyyy-MM-dd')
const currentStatus = ref('Read')
const currentSources = ref([])
const otherSourceEnabled = ref(false)
const otherSourceName = ref('')
const currentTopics = ref('')
const currentRemark = ref('')
const selectedFilter = ref('month')
const editingDate = ref(null)

const fetchStatuses = async () => {
  try {
    const response = await axios.get(`${API_URL}/statuses/`)
    statuses.value = response.data
  } catch (error) {
    console.error('Error fetching statuses:', error)
  }
}

const submitStatus = async () => {
  if (!currentStatus.value) return
  
  // Prepare sources string
  let finalSources = [...currentSources.value]
  if (otherSourceEnabled.value && otherSourceName.value.trim()) {
    finalSources.push(otherSourceName.value.trim())
  }

  try {
    const dateToSubmit = editingDate.value || today
    await axios.post(`${API_URL}/statuses/`, {
      date: dateToSubmit,
      status: currentStatus.value,
      sources: finalSources.join(', '),
      key_topics: currentTopics.value,
      remark: currentRemark.value
    })
    resetForm()
    fetchStatuses()
  } catch (error) {
    console.error('Error submitting status:', error)
  }
}

const resetForm = () => {
  currentStatus.value = 'Read'
  currentSources.value = []
  otherSourceEnabled.value = false
  otherSourceName.value = ''
  currentTopics.value = ''
  currentRemark.value = ''
  editingDate.value = null
}

const deleteStatus = async (date) => {
  if (!confirm(`Delete entry for ${date}?`)) return
  try {
    await axios.delete(`${API_URL}/statuses/${date}`)
    fetchStatuses()
  } catch (error) {
    console.error('Error deleting status:', error)
  }
}

const editStatus = (status) => {
  currentStatus.value = status.status || 'Read'
  
  const allSources = status.sources ? status.sources.split(', ').filter(s => s) : []
  currentSources.value = allSources.filter(s => AVAILABLE_SOURCES.includes(s))
  
  const customSources = allSources.filter(s => !AVAILABLE_SOURCES.includes(s))
  if (customSources.length > 0) {
    otherSourceEnabled.value = true
    otherSourceName.value = customSources.join(', ')
  } else {
    otherSourceEnabled.value = false
    otherSourceName.value = ''
  }

  currentTopics.value = status.key_topics || ''
  currentRemark.value = status.remark || ''
  editingDate.value = status.date
}

const filteredStatuses = computed(() => {
  const now = new Date()
  return statuses.value.filter(s => {
    const statusDate = parseISO(s.date)
    if (selectedFilter.value === 'all') return true
    if (selectedFilter.value === 'week') return isSameWeek(statusDate, now, { weekStartsOn: 1 })
    if (selectedFilter.value === 'month') return isSameMonth(statusDate, now)
    if (selectedFilter.value === 'year') return isSameYear(statusDate, now)
    return true
  })
})

onMounted(() => {
  fetchStatuses()
})
</script>

<template>
  <div class="tracker-card">
    <div class="header">
      <BookOpen class="logo-icon" size="32" />
      <h1>UPSC Current Affairs Tracker</h1>
    </div>
    <p class="today-date">Today's Date: {{ format(new Date(), 'dd-MM-yyyy') }}</p>

    <div class="input-section">
      <div class="section-title">
        <Layers size="18" />
        <h3>{{ editingDate ? 'Edit Status for ' + editingDate : 'Add Today\'s Status' }}</h3>
      </div>
      
      <div class="form-group">
        <label>Reading Status</label>
        <div class="status-toggle">
          <button 
            v-for="opt in STATUS_OPTIONS" 
            :key="opt"
            @click="currentStatus = opt"
            :class="['toggle-btn', { active: currentStatus === opt }, opt.toLowerCase().replace(' ', '-')]"
          >
            {{ opt }}
          </button>
        </div>
      </div>

      <div class="form-group">
        <label>Sources Tracked</label>
        <div class="sources-grid">
          <label v-for="source in AVAILABLE_SOURCES" :key="source" class="checkbox-label">
            <input type="checkbox" :value="source" v-model="currentSources" />
            <span>{{ source }}</span>
          </label>
          <label class="checkbox-label" :class="{ 'other-active': otherSourceEnabled }">
            <input type="checkbox" v-model="otherSourceEnabled" />
            <span>Other</span>
          </label>
        </div>
        
        <div v-if="otherSourceEnabled" class="other-source-input mt-2">
          <div class="input-with-icon">
            <PlusCircle size="16" class="icon" />
            <input 
              v-model="otherSourceName" 
              type="text" 
              placeholder="Enter custom source name(s)"
              class="small-input"
            />
          </div>
        </div>
      </div>

      <div class="form-group">
        <label>Key Topics Covered</label>
        <textarea 
          v-model="currentTopics" 
          placeholder="Major topics (e.g. SC Judgement on Privacy, RBI Repo Rate...)"
          rows="2"
        ></textarea>
      </div>

      <div class="form-group">
        <label>Daily Remark</label>
        <div class="remark-input">
          <MessageSquare size="18" class="icon" />
          <input 
            v-model="currentRemark" 
            type="text" 
            placeholder="How was the prep today? Any challenges?"
          />
        </div>
      </div>

      <div class="form-actions">
        <button @click="submitStatus" class="btn-primary">
          <component :is="editingDate ? Edit2 : Plus" size="18" />
          {{ editingDate ? 'Update Entry' : 'Add Entry' }}
        </button>
        <button v-if="editingDate" @click="resetForm" class="btn-secondary">
          Cancel
        </button>
      </div>
    </div>

    <div class="filter-section">
      <div class="filter-buttons">
        <button 
          v-for="filter in ['week', 'month', 'year', 'all']" 
          :key="filter"
          @click="selectedFilter = filter"
          :class="{ active: selectedFilter === filter }"
        >
          {{ filter.charAt(0).toUpperCase() + filter.slice(1) }}
        </button>
      </div>
    </div>

    <div class="list-section">
      <h2>History Log</h2>
      <ul v-if="filteredStatuses.length > 0">
        <li v-for="s in filteredStatuses" :key="s.date" :class="s.status.toLowerCase().replace(/\s+/g, '-')">
          <div class="status-content">
            <div class="status-header">
              <span class="date">{{ format(parseISO(s.date), 'dd MMMM yyyy') }}</span>
              <span :class="['status-badge', s.status.toLowerCase().replace(' ', '-')]">{{ s.status }}</span>
            </div>
            
            <div v-if="s.sources" class="sources-tags">
              <span v-for="source in s.sources.split(', ')" :key="source" class="source-tag">
                {{ source }}
              </span>
            </div>

            <div v-if="s.key_topics" class="topics-preview">
              <p><strong>Topics:</strong> {{ s.key_topics }}</p>
            </div>

            <div v-if="s.remark" class="remark-preview">
              <MessageSquare size="14" />
              <span>{{ s.remark }}</span>
            </div>
          </div>
          
          <div class="actions">
            <button @click="editStatus(s)" class="btn-icon" title="Edit">
              <Edit2 size="16" />
            </button>
            <button @click="deleteStatus(s.date)" class="btn-icon btn-delete" title="Delete">
              <Trash2 size="16" />
            </button>
          </div>
        </li>
      </ul>
      <p v-else class="empty-state">No records found for this period.</p>
    </div>
  </div>
</template>

<style scoped>
.tracker-card {
  max-width: 700px;
  margin: 0 auto;
  background: var(--bg-card, #fff);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  color: #333;
}

.header { display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 0.25rem; }
.logo-icon { color: #42b883; }
h1 { margin: 0; color: #2c3e50; font-size: 1.8rem; }
.today-date { color: #666; margin-bottom: 2rem; font-weight: 500; text-align: center; }

.section-title { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem; color: #42b883; }
.section-title h3 { margin: 0; }

.input-section { 
  margin-bottom: 2.5rem; 
  text-align: left; 
  background: #f8fafc; 
  padding: 1.5rem; 
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.form-group { margin-bottom: 1.25rem; }
.form-group label { display: block; font-weight: 600; margin-bottom: 0.5rem; font-size: 0.9rem; color: #475569; }

input[type="text"], textarea { 
  width: 100%; 
  padding: 0.75rem; 
  border: 1px solid #cbd5e1; 
  border-radius: 8px; 
  font-size: 1rem;
  box-sizing: border-box;
}

textarea { resize: vertical; }

.small-input {
  padding: 0.5rem 0.75rem !important;
  font-size: 0.9rem !important;
}

.mt-2 { margin-top: 0.5rem; }

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.input-with-icon .icon {
  position: absolute;
  left: 0.75rem;
  color: #94a3b8;
}

.input-with-icon input {
  padding-left: 2.5rem !important;
}

.status-toggle {
  display: flex;
  gap: 0.5rem;
  background: #e2e8f0;
  padding: 0.25rem;
  border-radius: 10px;
}

.toggle-btn {
  flex: 1;
  padding: 0.6rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 700;
  color: #64748b;
  background: transparent;
  transition: all 0.2s;
}

.toggle-btn.active {
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.toggle-btn.active.read { color: #42b883; }
.toggle-btn.active.partial { color: #f59e0b; }
.toggle-btn.active.not-read { color: #ef4444; }

.remark-input {
  position: relative;
  display: flex;
  align-items: center;
}

.remark-input .icon {
  position: absolute;
  left: 0.75rem;
  color: #94a3b8;
}

.remark-input input {
  padding-left: 2.5rem;
}

.sources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 0.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.85rem;
  background: white;
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s;
}

.checkbox-label:hover { border-color: #42b883; }
.checkbox-label.other-active { border-color: #42b883; background: #f0fdf4; }

.form-actions { display: flex; gap: 0.75rem; margin-top: 1.5rem; }

button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
  border: none;
}

.btn-primary { background: #42b883; color: white; }
.btn-primary:hover { background: #3aa876; transform: translateY(-1px); }
.btn-secondary { background: #94a3b8; color: white; }

.btn-icon { background: transparent; padding: 0.5rem; color: #64748b; }
.btn-icon:hover { color: #42b883; background: #f0fdf4; }
.btn-delete:hover { color: #ef4444; background: #fef2f2; }

.filter-section { margin-bottom: 2rem; }
.filter-buttons { display: flex; gap: 0.5rem; justify-content: center; }
.filter-buttons button {
  padding: 0.5rem 1.25rem;
  background: #f1f5f9;
  color: #64748b;
  font-size: 0.9rem;
}
.filter-buttons button.active { background: #42b883; color: white; }

.list-section h2 { text-align: left; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.75rem; margin-bottom: 1.5rem; color: #1e293b; }
ul { list-style: none; padding: 0; }
li {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.25rem;
  margin-bottom: 1rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  border-left: 5px solid #cbd5e1;
  transition: transform 0.2s;
}
li:hover { transform: translateX(4px); }

li.read { border-left-color: #42b883; }
li.partial { border-left-color: #f59e0b; }
li.not-read { border-left-color: #ef4444; }

.status-content { flex: 1; text-align: left; }
.status-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem; }
.date { font-weight: 700; color: #1e293b; font-size: 1rem; }
.status-badge { 
  background: #f1f5f9; 
  padding: 0.2rem 0.6rem; 
  border-radius: 20px; 
  font-size: 0.75rem; 
  font-weight: 700;
  text-transform: uppercase;
}

.status-badge.read { background: #f0fdf4; color: #166534; }
.status-badge.partial { background: #fffbeb; color: #92400e; }
.status-badge.not-read { background: #fef2f2; color: #991b1b; }

.sources-tags { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 0.75rem; }
.source-tag { 
  background: #ecfdf5; 
  color: #065f46; 
  font-size: 0.7rem; 
  padding: 0.1rem 0.5rem; 
  border-radius: 4px;
  border: 1px solid #a7f3d0;
}

.topics-preview { 
  background: #f8fafc; 
  padding: 0.75rem; 
  border-radius: 6px; 
  font-size: 0.9rem; 
  color: #475569;
  line-height: 1.4;
  margin-bottom: 0.5rem;
}
.topics-preview p { margin: 0; white-space: pre-wrap; }

.remark-preview {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #64748b;
  font-style: italic;
}

.actions { display: flex; gap: 0.25rem; margin-left: 1rem; }

.empty-state { color: #94a3b8; font-style: italic; text-align: center; padding: 2rem; }

@media (prefers-color-scheme: dark) {
  .tracker-card { background: #0f172a; color: #f1f5f9; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3); }
  h1 { color: #42b883; }
  .today-date { color: #94a3b8; }
  .input-section { background: #1e293b; border-color: #334155; }
  .status-toggle { background: #0f172a; }
  .toggle-btn { color: #94a3b8; }
  .toggle-btn.active { background: #1e293b; color: white; }
  .form-group label { color: #94a3b8; }
  input[type="text"], textarea { background: #0f172a; border-color: #334155; color: white; }
  .checkbox-label { background: #0f172a; border-color: #334155; color: #cbd5e1; }
  li { background: #1e293b; border-color: #334155; }
  .date { color: #f1f5f9; }
  .topics-preview { background: #0f172a; color: #cbd5e1; }
  .list-section h2 { border-bottom-color: #334155; color: #f1f5f9; }
  .filter-buttons button { background: #334155; color: #94a3b8; }
  .source-tag { background: #064e3b; color: #a7f3d0; border-color: #065f46; }
  .remark-preview { color: #94a3b8; }
}
</style>
