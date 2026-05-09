<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { format, isSameWeek, isSameMonth, isSameYear, parseISO } from 'date-fns'
import { Trash2, Edit2, Plus, Calendar } from 'lucide-vue-next'

const API_URL = 'http://localhost:8001'

const statuses = ref([])
const today = format(new Date(), 'yyyy-MM-dd')
const currentStatus = ref('')
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
  
  try {
    const dateToSubmit = editingDate.value || today
    await axios.post(`${API_URL}/statuses/`, {
      date: dateToSubmit,
      status: currentStatus.value
    })
    currentStatus.value = ''
    editingDate.value = null
    fetchStatuses()
  } catch (error) {
    console.error('Error submitting status:', error)
  }
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
  currentStatus.value = status.status
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
    <h1>Daily Current Affairs Tracker</h1>
    <p class="today-date">Today's Date: {{ format(new Date(), 'dd-MM-yyyy') }}</p>

    <div class="input-section">
      <h3>{{ editingDate ? 'Edit Status for ' + editingDate : 'Add Today\'s Status' }}</h3>
      <div class="input-group">
        <input 
          v-model="currentStatus" 
          type="text" 
          placeholder="e.g., Read, Not Read, Completed"
          @keyup.enter="submitStatus"
        />
        <button @click="submitStatus" class="btn-primary">
          <component :is="editingDate ? Edit2 : Plus" size="18" />
          {{ editingDate ? 'Update' : 'Add' }}
        </button>
        <button v-if="editingDate" @click="editingDate = null; currentStatus = ''" class="btn-secondary">
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
      <h2>History</h2>
      <ul v-if="filteredStatuses.length > 0">
        <li v-for="s in filteredStatuses" :key="s.date" :class="s.status.toLowerCase().replace(/\s+/g, '-')">
          <div class="status-info">
            <span class="date">{{ format(parseISO(s.date), 'dd-MM-yyyy') }}</span>
            <span class="status-text">{{ s.status }}</span>
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
  max-width: 600px;
  margin: 0 auto;
  background: var(--bg-card, #fff);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  color: #333;
}

h1 { margin-bottom: 0.5rem; color: #2c3e50; }
.today-date { color: #666; margin-bottom: 2rem; font-weight: 500; }

.input-section { margin-bottom: 2rem; text-align: left; }
.input-group { display: flex; gap: 0.5rem; margin-top: 0.5rem; }
input { 
  flex: 1; 
  padding: 0.75rem; 
  border: 1px solid #ddd; 
  border-radius: 6px; 
  font-size: 1rem;
}

button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
  border: none;
}

.btn-primary { background: #42b883; color: white; }
.btn-primary:hover { background: #3aa876; }
.btn-secondary { background: #666; color: white; }
.btn-icon { background: transparent; padding: 0.4rem; color: #666; }
.btn-icon:hover { color: #42b883; background: #f0fdf4; }
.btn-delete:hover { color: #ef4444; background: #fef2f2; }

.filter-section { margin-bottom: 1.5rem; }
.filter-buttons { display: flex; gap: 0.5rem; justify-content: center; }
.filter-buttons button {
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  color: #4b5563;
}
.filter-buttons button.active {
  background: #42b883;
  color: white;
}

.list-section h2 { text-align: left; border-bottom: 2px solid #eee; padding-bottom: 0.5rem; margin-bottom: 1rem; }
ul { list-style: none; padding: 0; }
li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  background: #f9fafb;
  border-radius: 8px;
  border-left: 4px solid #ddd;
}

li.read { border-left-color: #42b883; }
li.not-read { border-left-color: #ef4444; }

.status-info { display: flex; flex-direction: column; align-items: flex-start; }
.date { font-size: 0.85rem; color: #888; }
.status-text { font-weight: 600; }
.actions { display: flex; gap: 0.25rem; }

.empty-state { color: #999; font-style: italic; }

@media (prefers-color-scheme: dark) {
  .tracker-card { background: #1a1a1a; color: #e5e7eb; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4); }
  h1 { color: #42b883; }
  .today-date { color: #9ca3af; }
  input { background: #2d2d2d; border-color: #444; color: white; }
  li { background: #2d2d2d; }
  .list-section h2 { border-bottom-color: #444; }
  .filter-buttons button { background: #374151; color: #d1d5db; }
  .btn-icon { color: #9ca3af; }
}
</style>
